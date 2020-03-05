import copy

import pytest

from trict.util import (flatten_dict, iter_keys, leaves, recursive_delete,
                        recursive_set, traverse)

def base_dict():
    return {
        'user': {
            'information': {
                'attribute': 'infonugget',
                'another_attribute': 'secondnugget'
            },
            'moreinformation': 'extranugget'
        }
    }

def test_recursive_set_sets():
    d = {}
    recursive_set(d, ['test', 'attribute'], 'value')
    assert d == {
        'test': {
            'attribute': 'value'
        }
    }
    recursive_set(d, ['test', 'anotherattribute'], 'value')
    assert d == {
        'test': {
            'attribute': 'value',
            'anotherattribute': 'value',
        }
    }
    recursive_set(d, ['test', 'attribute'], 'value2')
    assert d == {
        'test': {
            'attribute': 'value2',
            'anotherattribute': 'value',
        }
    }
    recursive_set(d, ['test2'], 'value2')
    assert d == {
        'test': {
            'attribute': 'value2',
            'anotherattribute': 'value',
        },
        'test2': 'value2'
    }

def test_recursive_delete_dels():
    d = base_dict()
    recursive_delete(d, ['user', 'information', 'attribute'])
    assert d == {
        'user': {
            'information': {
                'another_attribute': 'secondnugget'
            },
            'moreinformation': 'extranugget'
        }
    }
    recursive_delete(d, ['user', 'information', 'another_attribute'])
    assert d == {
        'user': {
            'information': {},
            'moreinformation': 'extranugget'
        }
    }

def test_recursive_delete_throws():
    d = base_dict()
    recursive_delete(d, ['user', 'information', 'attribute'])
    old_d = copy.deepcopy(d)
    with pytest.raises(KeyError):
        recursive_delete(d, ['user', 'information', 'attribute'])
    assert d == old_d

def test_flatten_dict_flattens():
    d = base_dict()
    old_d = copy.deepcopy(d)
    assert flatten_dict(d) == {
            'user.information.attribute': 'infonugget',
            'user.information.another_attribute': 'secondnugget',
            'user.moreinformation': 'extranugget'
    }
    assert d == old_d

def test_flatten_dict_throws():
    d = {
        'user': {
            'information': {
                'attr.ibute': 'infonugget', # Note extra period
                'another_attribute': 'secondnugget'
            },
            'moreinformation': 'extranugget'
        }
    }
    old_d = copy.deepcopy(d)
    with pytest.raises(ValueError, 
        match=r"Separator \".\" found in a subkey in path \['user', 'information', 'attr.ibute'\]"
        ):
        flatten_dict(d)
    assert d == old_d

def test_traverse():
    d = base_dict()
    old_d = copy.deepcopy(d)
    assert [n for n in traverse(d)] == [
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
    assert d == old_d
    assert [k for k in traverse(d, keys_only=True)] == [
        ['user'],
        ['user', 'information'],
        ['user', 'information', 'attribute'],
        ['user', 'information', 'another_attribute'],
        ['user', 'moreinformation'],
    ]
    assert d == old_d

def test_leaves():
    d = base_dict()
    old_d = copy.deepcopy(d)
    assert [l for l in leaves(d)] == [
        (['user', 'information', 'attribute'], 'infonugget'), 
        (['user', 'information', 'another_attribute'], 'secondnugget'), 
        (['user', 'moreinformation'], 'extranugget')
    ]
    assert d == old_d

def test_iter_keys():
    d = base_dict()
    assert [k for k in iter_keys(d)] == [
        'user', 
        'information', 
        'attribute', 
        'another_attribute', 
        'moreinformation'
    ]
