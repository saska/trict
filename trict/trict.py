import sys
from collections import UserDict
from functools import reduce

from .util import (flatten_dict, iter_keys, recursive_delete, recursive_set,
                  leaves, traverse)


class Trict(UserDict):
    """Trict (Tricky dict).

    Args:
        initialdata: dict
        key_sep: str, used to separate keys when key lists
            want to be made into single strings

    Alternate constructors:
        Args are only documented if their usage differs
        from default constructor.

        from_flatten_dict:
            Args:
                flat_dict: Flattened dictionary with 
                    string-separated key paths. If contains
                    nested dictionaries, those are passed as-is
                key_sep: Separator, used for parsing the keys
                    of flat_dict as well as their default usage
    """

    def __init__(self, initialdata, key_sep='.'):
        if key_sep is not None and type(key_sep) is not str:
            raise TypeError('key_sep must be str or None')
        for k in iter_keys(initialdata):
            if key_sep in k:
                raise ValueError(f'key_sep found in key {k}')
        self.key_sep = key_sep
        super().__init__(initialdata)

    @classmethod
    def from_flat_dict(cls, flat_dict, key_sep='.', **kwargs):
        d = {}
        for k, v in flat_dict.items():
            recursive_set(d, k.split(key_sep), v)
        return cls(d, key_sep=key_sep, **kwargs)

    def __getitem__(self, key):
        key = self.key_to_list(key)
        try:
            return reduce(lambda x, y: x[y], key, self.data)
        except KeyError:
            raise KeyError(f"Path not found: {key}")

    def __setitem__(self, key, val):
        """See util.recursive_set"""
        key = self.key_to_list(key)
        recursive_set(self.data, key, val)

    def __delitem__(self, key):
        """See util.recursive_delete"""
        key = self.key_to_list(key)
        recursive_delete(self.data, key)

    def __contains__(self, key):
        key = self.key_to_list(key)
        return key in self.traverse(keys_only=True)

    def get(self, key, default=None):
        try:
            self.__getitem__(key)
        except KeyError:
            return default

    def key_to_list(self, key):
        if type(key) is not list:
            if type(key) is not str:
                raise TypeError('Key is not list or str')
            key = key.split(self.key_sep)
        return key

    def flatten(self):
        """See util.flatten_dict"""
        sep = '.' if self.key_sep is None else self.key_sep
        return flatten_dict(self.data, sep=sep)

    def traverse(self, *args, **kwargs):
        """See util.traverse"""
        yield from traverse(self.data, *args, **kwargs)

    def leaves(self):
        """See util.leaves"""
        yield from leaves(self.data)

    def get_by_list(self, keys, strict=False):
        """
        Note that simple lists of indenting keys
        can be fed straight to __getitem__, this is a 
        helper method to try and find any value in a list of keys.
        
        args:
            keys:
                list (of str or list), keys to try and find

            strict:
                bool, if True, throws when no keys are found (default False,
                returns None instead).

        returns:
            val from key if any key found or None if none found
            and strict == False.
        """
        for k in keys:
            try:
                return self.__getitem__(k)
            except KeyError:
                continue
        if strict:
            raise KeyError(f'No key in {keys} found')
        return None
    
    def map_leaves(self, callable_):
        # TODO maybe we should actually call this with 
        # key, value so you could do more cool stuff?
        for k, v in self.leaves():
            self.__setitem__(k, callable_(v))
        return self

    def map_with_dict(self, mapper_dict, strict=False):
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
                dict, 
                {
                    key: [mapping1, mapping2],
                    key2: [mapping3.submapping4, mapping4, ..., mappingN]
                }

            strict:
                bool, If True, throws on unfound mapping (passed to self.get_by_list).
                Default False - returns None instead.

        returns:
            {
                key (from mapper_dict): value (from self) if any mapping matched
            }
        """
        self.data = {
            k: self.get_by_list(
                v, 
                strict=strict
            ) for k, v in mapper_dict.items()
        }
        return self
