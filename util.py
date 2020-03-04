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


def flatten_dict(d, sep='.', max_depth=sys.getrecursionlimit(), prefix='',  level=0):
    """Flatten a dictionary.
    
    Args:
        d:
            dict, dictionary to flatten
        sep:
            str, separator character(s) in keys
        max_depth:
            int, maximum recursion depth
        prefix:
            Prefix to prepend to key, used in recursion
        level:
            Level of recursion, used in recursion

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
    ret_d = copy.deepcopy(d)
    for k, v in d.items():
        if not isinstance(k, str):
            k = str(k)
            if sep in k:
                raise ValueError(f'String representation "{k}" contains sep "{sep}"')
        new_k = k if level == 0 else sep.join([prefix, k])
        if isinstance(v, dict) and (level < max_depth):
            v = ret_d.pop(k)
            ret_d.update(flatten_dict(v, sep, max_depth, new_k, level + 1))
        else:
            # if non-dict v at top level no need to do anything
            if level != 0:
                v = ret_d.pop(k)
                ret_d[new_k] = v

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

def traverse(d, sep='.', prefix=''):
    """Traverses through dictionary.

    Yields 2-tuples of (sep-separated key path, value).

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
        >>> [k for k in traverse(d)]
        [
            ('user.information.attribute', 'infonugget'), 
            ('user.information.another_attribute', 'secondnugget'), 
            ('user.moreinformation', 'extranugget')
        ]
    """
    # TODO this should probably have a lot of the safety stuff of flatten_dict
    # Or flatten_dict should have none either, depends on design philosophy I guess
    for k, v in d.items():
        new_k = k if prefix == '' else sep.join([prefix, k])
        if isinstance(v, dict):
            yield from traverse(v, prefix=new_k)
        else:
            yield new_k, v
