import sys
import copy 

def recursive_set(d, attr_list, val):
    """Recursively sets dictionary values. Will create non-existant keys
    params:
        d: dictionary to set values in
        attr_list: list of nested keys
        val: value to set

    Example usage:
        >>> d = {}
        >>> attr_list = 'user.information.attribute'.split('.')
        >>> val = 'infonugget'
        >>> recursive_set(d, attr_list, val)
        >>> d
        {
            'user': {
                'information': {
                    'attribute': 'infonugget'
                }
            }
        }
    """
    if len(attr_list) == 1:
        d[attr_list[0]] = val
    else:
        try:
            root = d[attr_list[0]]
            recursive_set(root, attr_list[1:], val)
        except KeyError:
            d[attr_list[0]] = {}
            recursive_set(d[attr_list[0]], attr_list[1:], val)

def recursive_delete(d, attr_list):
    if len(attr_list) == 1:
        del d[attr_list[0]]
    else:
        root = d[attr_list[0]]
        recursive_delete(root, attr_list[1:])

def flatten_dict(d, sep='.', check_keys=True):
    """Flatten a dictionary.

    Args:
        d:
            dict, dictionary to flatten
        sep:
            str, separator character(s) in keys
        check_keys:
            bool, if True will throw if a key in
            d already contains sep

    Example usage:
        >>> d = {
                'user': {
                    'information': {
                        'attribute': 'infonugget',
                        'another_attribute': 'secondnugget'
                    },
                    'moreinformation': 'extranugget'
                }
            }
        >>> flatten_dict(d)
        {
            'user.information.attribute': 'infonugget',
            'user.information.another_attribute': 'secondnugget',
            'user.moreinformation': 'extranugget'
        }
    """
    ret_d = {}
    for k, v in leaves(d):
        if check_keys and any([sep in subkey for subkey in k]):
            raise ValueError(f'Separator "{sep}" found in a subkey in path {k}')
        ret_d[sep.join(k)] = v 
    return ret_d

def iter_keys(d):
    """Recursively iterate through all keys at any level.

    Example usage:
        >>> d = {
                'user': {
                    'information': {
                        'attribute': 'infonugget',
                        'another_attribute': 'secondnugget'
                    },
                    'moreinformation': 'extranugget'
                }
            }
        >>> [k for k in iter_keys(d)]
        ['user', 'information', 'attribute', 'another_attribute', 'moreinformation']
    """
    for k, v in d.items():
        yield(k)
        if isinstance(v, dict):
            yield from iter_keys(v)

def leaves(d, prev=[]):
    """Returns leaves of dictionary and their keys.

    Yields 2-tuples of (key path as list, value).

    Example usage:
        >>> d = {
                'user': {
                    'information': {
                        'attribute': 'infonugget',
                        'another_attribute': 'secondnugget'
                    },
                    'moreinformation': 'extranugget'
                }
            }
        >>> [l for l in leaves(d)]
        [
            (['user', 'information', 'attribute'], 'infonugget'), 
            (['user', 'information', 'another_attribute'], 'secondnugget'), 
            (['user', 'moreinformation'], 'extranugget')
        ]
    """
    for k, v in d.items():
        new_k = [k] if prev == [] else prev + [k]
        if isinstance(v, dict):
            yield from leaves(v, prev=new_k)
        else:
            yield new_k, v

def traverse(d, keys_only=False, prev=[]):
    """Traverses through dictionary.

    Yields 2-tuples of (key path as list, value)
    for each node.

    If keys_only=True, only yields keys.

    Example usage:
        >>> d = {
                    'user': {
                        'information': {
                            'attribute': 'infonugget',
                            'another_attribute': 'secondnugget'
                        },
                        'moreinformation': 'extranugget'
                    }
                }
        >>> [n for n in traverse(d)]
        [
            (
                ['user'], {
                    'information': {
                        'attribute': 'infonugget', 
                        'another_attribute': 'secondnugget'
                    }, 
                    'moreinformation': 'extranugget'
                }
            ), (
                ['user', 'information'], {
                    'attribute': 'infonugget', 
                    'another_attribute': 'secondnugget'
                }
            ), (
                ['user', 'information', 'attribute'], 'infonugget'
            ), (
                ['user', 'information', 'another_attribute'], 'secondnugget'
            ), (
                ['user', 'moreinformation'], 'extranugget'
            )
        ]

    """
    for k, v in d.items():
        new_k = [k] if prev == [] else prev + [k]
        if keys_only:
            yield new_k
        else:
            yield new_k, v
        if isinstance(v, dict):
            yield from traverse(v, keys_only=keys_only, prev=new_k)
