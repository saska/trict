import sys
from collections import UserDict
from functools import reduce

from .util import (flatten_dict, iter_keys, recursive_delete, recursive_set,
                  leaves)


class Trict(UserDict):
    def __init__(self, initialdata, key_sep='.', strict_get=True):
        if key_sep is not None and type(key_sep) is not str:
            raise TypeError('key_sep must be str or None')
        for k in iter_keys(initialdata):
            if key_sep in k:
                raise ValueError(f'key_sep found in key {k}')
        self.key_sep = key_sep
        self.strict_get = strict_get
        super().__init__(initialdata)

    def __getitem__(self, key):
        key = self.key_to_list(key)
        try:
            val = reduce(lambda x, y: x[y], key, self.data)
        except KeyError as e:
            if self.strict_get:
                raise KeyError(f"Path not found: {key}")
            else:
                val = None
        return val

    def __setitem__(self, key, val):
        """See util.recursive_set"""
        key = self.key_to_list(key)
        recursive_set(self.data, key, val)

    def __delitem__(self, key):
        """See util.recursive_delete"""
        key = self.key_to_list(key)
        recursive_delete(self.data, key)

    def key_to_list(self, key):
        if type(key) is not list:
            if type(key) is not str:
                raise TypeError('Key is not list or str')
            key = key.split(self.key_sep)
        return key

    def flatten(self, max_depth=sys.getrecursionlimit()):
        """See util.flatten_dict"""
        sep = '.' if self.key_sep is None else self.key_sep
        return flatten_dict(self.data, max_depth=max_depth, sep=sep)

    def traverse(self):
        """See util.traverse"""
        sep = '.' if self.key_sep is None else self.key_sep
        yield from traverse(self.data, sep=sep)

    def map_leaves(self, callable_):
        for k, v in self.traverse():
            self.__setitem__(k, callable_(v))

    def leaves(self):
        """See util.leaves"""
        yield from leaves(self.data)

    def get_by_list(self, keys):
        """
        Note that simple lists of indenting keys
        can be fed straight to __getitem__, this is a 
        helper method to try and find any value in a list of keys.
        
        args:
            keys:
                list of str or list

        returns:
            val from key if any key found or None if none found
            and self.strict_get == False.
        """
        for k in keys:
            try:
                return self.__getitem__(k)
            except KeyError:
                continue
        if self.strict_get:
            raise KeyError(f'No key in {keys} found')
        return None

    def map_with_dict(self, mapper_dict):
        """Map values in trict to new dictionary.

        Use-case not clear so will give example:
            You want to harmonize data from multiple sources with
            different structures but you know the path to the same
            data point in each one. You can create a mapper dict
            for them and just throw whatever documents you receive into 
            a trict, then map them to the same format with this method.
            If you get a new data source, add stuff to your mapping dict
            (Making sure they don't have different data points in the same path obv).

        Args:
            mapper_dict:
                {
                    key: [mapping1, mapping2],
                    key2: [mapping3, mapping4, ..., mappingN]
                }
        returns:
            {
                key (from mapper_dict): value (from self) if any mapping matched
            }
        """
        ret_d = {}
        return {k: self.get_by_list(v) for k, v in mapper_dict.items()}
