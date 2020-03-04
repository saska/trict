import sys
from functools import reduce
from collections import UserDict
from util import recursive_set, flatten_dict, iter_keys, traverse

class FancyDict(UserDict):
    def __init__(self, initialdata, key_sep='.', strict_get=True):
        if key_sep is not None and type(key_sep) is not str:
            raise TypeError('key_sep must be str or None')
        for k in iter_keys(initialdata):
            if key_sep in k:
                raise ValueError(f'key_sep found in key {k}')
        self.key_sep = key_sep
        super().__init__(initialdata)

    def __getitem__(self, key):
        if type(key) is not list:
            if type(key) is not str:
                raise TypeError('Key is not list or str')
            key = key.split(self.key_sep)
        try:
            val = reduce(lambda x, y: x[y], key, self.data)
        except KeyError as e:
            if self.strict_get:
                raise KeyError(f"Path not found: {key}")
            else:
                val = None
        return val

    def __setitem__(self, key, val):
        if type(key) is not list:
            if type(key) is not str:
                raise TypeError('Key is not list or str')
            key = key.split(self.key_sep)
        recursive_set(self.data, key, val)
    
    def flatten(self, max_depth=sys.getrecursionlimit()):
        sep = '.' if self.key_sep is None else self.key_sep
        return flatten_dict(self.data, max_depth=max_depth, sep=sep)

    def traverse(self):
        sep = '.' if self.key_sep is None else self.key_sep
        yield from traverse(self.data, sep=sep)

    def map_leaves(self, callable_):
        for k, v in self.traverse():
            self.__setitem__(k, callable_(v))
