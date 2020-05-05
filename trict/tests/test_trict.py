import copy

import pytest

from trict import Trict
from trict.tests.helpers import base_dict, invalid_base_dict


def test_trict_init_inits():
    tr = Trict(base_dict()) # pylint: disable=unused-variable

def test_trict_init_throws():
    with pytest.raises(ValueError,
        match='key_sep found in key attr.ibute'
        ):
        tr = Trict(invalid_base_dict()) # pylint: disable=unused-variable

def test_trict_getter_gets():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    assert tr['user.information.attribute'] == 'infonugget'
    assert tr[['user', 'information', 'attribute']] == 'infonugget'
    assert tr.data == old_data

def test_strict_trict_getter_throws():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    with pytest.raises(KeyError):
        tr['user.information.notanattribute']
    with pytest.raises(KeyError):
        tr[['user', 'information', 'notanattribute']]
    assert tr.data == old_data

def test_nonstrict_trict_getter_not_throws():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    assert tr.get('user.information.notanattribute') == None
    assert tr.get(['user', 'information', 'notanattribute']) == None
    assert tr.data == old_data

def test_trict_setter_sets():
    tr = Trict(base_dict())
    tr['user.superinformation.superattribute'] = 'super'
    tr[['user', 'hyperinformation', 'hyperattribute']] = 'hyper'
    assert tr.data == {
        'user': {
            'information': {
                'attribute': 'infonugget',
                'another_attribute': 'secondnugget'
            },
            'moreinformation': 'extranugget',
            'superinformation': {
                'superattribute': 'super',
            },
            'hyperinformation': {
                'hyperattribute': 'hyper',
            },
        }
    }
    tr['user.information.attribute'] = 'differentnugget'
    tr[['user', 'information', 'another_attribute']] = 'thirdnugget' 
    assert tr.data == {
        'user': {
            'information': {
                'attribute': 'differentnugget',
                'another_attribute': 'thirdnugget'
            },
            'moreinformation': 'extranugget',
            'superinformation': {
                'superattribute': 'super',
            },
            'hyperinformation': {
                'hyperattribute': 'hyper',
            },
        }
    }

def test_trict_deleter_deletes():
    tr = Trict(base_dict())
    del tr['user.information']
    assert tr.data == {
        'user': {
            'moreinformation': 'extranugget'
        }
    }
    del tr[['user', 'moreinformation']]
    assert tr.data == {
        'user': {}
    }

def test_trict_deleter_throws():
    tr = Trict(base_dict())
    with pytest.raises(KeyError):
        del tr['user.information.nonexistantattribute']
    with pytest.raises(KeyError):
        del tr['user.information.nonexistantattribute']

def test_trict_contains():
    tr = Trict(base_dict())
    for key in [
        'user.information',
        'user.information.another_attribute',
        ['user', 'moreinformation']
    ]:
        assert key in tr

    for key in [
        'information.attribute',
        'doesntexist',
        ['nothing', 'here']
    ]:
        assert key not in tr

def test_key_to_list_lists():
    tr = Trict({})
    assert tr.key_to_list('i.j.k') == ['i', 'j', 'k']

def test_key_to_list_throws():
    tr = Trict({})
    with pytest.raises(TypeError):
        tr.key_to_list(1)

def test_get_by_list_finds():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    val = tr.get_by_list([
        'user.misinformation.attribute',
        'nonuser.noninformation.nonattribute',
        ['user', 'information', 'attribute']
    ]) 
    assert val == 'infonugget'
    assert tr.data == old_data
    val = tr.get_by_list([
        ['user', 'information', 'whatattribute'],
        ['user', 'information', 'nonattribute'],
        'user.information.another_attribute'
    ])
    assert val == 'secondnugget'
    assert tr.data == old_data

def test_strict_get_by_list_throws():
    tr = Trict(base_dict())
    with pytest.raises(KeyError):
        tr.get_by_list([
            'none.of.these',
            'i.mean.none',
            ['keys', 'exist']
        ], strict=True)

def test_nonstrict_get_by_list_not_throws():
    tr = Trict(base_dict())
    val = tr.get_by_list([
            'none.of.these',
            'i.mean.none',
            ['keys', 'exist']
        ])
    assert val == None 

def test_flatten_flats():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    assert tr.flatten() == {
            'user.information.attribute': 'infonugget',
            'user.information.another_attribute': 'secondnugget',
            'user.moreinformation': 'extranugget'
    }
    assert tr.data == old_data

def test_traverse_traverses():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    assert [n for n in tr.traverse()] == [
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
    assert tr.data == old_data
    assert [k for k in tr.traverse(keys_only=True)] == [
        ['user'],
        ['user', 'information'],
        ['user', 'information', 'attribute'],
        ['user', 'information', 'another_attribute'],
        ['user', 'moreinformation'],
    ]
    assert tr.data == old_data

def test_leaves():
    tr = Trict(base_dict())
    old_data = copy.deepcopy(tr.data)
    assert [l for l in tr.leaves()] == [
        (['user', 'information', 'attribute'], 'infonugget'), 
        (['user', 'information', 'another_attribute'], 'secondnugget'), 
        (['user', 'moreinformation'], 'extranugget')
    ]
    assert tr.data == old_data

def test_map_leaves_maps():
    tr = Trict(base_dict())
    tr.map_leaves(lambda x: x + ' and something more')
    assert tr.data == {
        'user': {
            'information': {
                'attribute': 'infonugget and something more',
                'another_attribute': 'secondnugget and something more'
            },
            'moreinformation': 'extranugget and something more'
        }
    }

def test_map_with_dict_maps():
    tr = Trict(base_dict())
    mapper = {
        'newkey': [
            'user.noninformation.nonattribute',
            'user.information.another_attribute'
        ],
        'othernewkey': [
            ['user', 'noninformation'],
            ['user', 'information']
        ]
    }
    assert tr.map_with_dict(mapper) == {
        'newkey': 'secondnugget',
        'othernewkey':  {
                'attribute': 'infonugget',
                'another_attribute': 'secondnugget'
        },
    }

def test_map_with_dict_throws():
    tr = Trict(base_dict())
    mapper = {
        'newkey': [
            ['none', 'of', 'these'],
            ['are', 'in', 'there']
        ]
    }
    with pytest.raises(KeyError):
        tr.map_with_dict(mapper, strict=True)


def test_nonstrict_map_with_dict_not_throws():
    tr = Trict(base_dict())
    mapper = {
        'newkey': [
            ['none', 'of', 'these'],
            ['are', 'in', 'there']
        ],
        'othernewkey': [
            'and.these.are',
            'not.either'
        ]
    }
    mapped = tr.map_with_dict(mapper)
    assert mapped == {
        'newkey': None,
        'othernewkey': None
    }

def test_from_flat_dict_inits():
    tr = Trict(base_dict())
    flat = tr.flatten()
    new_tr = Trict.from_flat_dict(flat)
    assert new_tr.data == tr.data

def test_from_flat_dict_with_nested_dict_inits():
    d = {
        'info.attribute': {
            'nugget'
        },
        'otherinfo': 'secondnugget'
    }
    tr = Trict.from_flat_dict(d)
    assert tr.data == {
        'info': {
            'attribute': {
                'nugget'
            }
        },
        'otherinfo': 'secondnugget'
    }

def test_repr():
    assert Trict({}).__repr__() == 'Trict({})'