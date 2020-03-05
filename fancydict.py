import sys
from functools import reduce
from collections import UserDict
from util import recursive_set, recursive_delete, flatten_dict, iter_keys, traverse

class FancyDict(UserDict):
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
        key = self.key_to_list(key)
        recursive_set(self.data, key, val)

    def __delitem__(self, key):
        key = self.key_to_list(key)
        recursive_delete(self.data, key)

    def key_to_list(self, key):
        if type(key) is not list:
            if type(key) is not str:
                raise TypeError('Key is not list or str')
            key = key.split(self.key_sep)
        return key

    def flatten(self, max_depth=sys.getrecursionlimit()):
        sep = '.' if self.key_sep is None else self.key_sep
        return flatten_dict(self.data, max_depth=max_depth, sep=sep)

    def traverse(self):
        sep = '.' if self.key_sep is None else self.key_sep
        yield from traverse(self.data, sep=sep)

    def map_leaves(self, callable_):
        for k, v in self.traverse():
            self.__setitem__(k, callable_(v))

    def get_by_list(self, keys):
        """
        Note that simple lists of indenting keys
        can be fed straight to __getitem__, this is a 
        helper method to try and find any value in a list of keys.
        Args:
            keys:
                list of str or list
        """
        for k in keys:
            try:
                return self.__getitem__(k)
            except KeyError:
                continue
        if self.strict_get:
            raise KeyError(f'No key in {keys} found')
        return None

    def map_with_mapper_dict(self, mapper_dict):
        """
        Since this seems useless-ish I'm going to defend myself.
        You want to harmonize data from multiple sources with
            different structures but you know the path to the same
            data point in each one. You can create a mapper dict
            for them and just throw whatever documents you receive into 
            a fancydict, then map them to the same format with this method.
            If you get a new data source, add stuff to your mapping dict.
            (Making sure they don't have different data points in the same path obv)
        Args:
            mapper_dict:
                {
                    key: [mappings],
                    key2: [more mappings]
                }
        returns:
            {
                key: value from self if any mapping matched
            }

        Useful when:
            - 
        """
        ret_d = {}
        return {k: self.get_by_list(v) for k, v in mapper_dict.items()}