[![Last release](https://anaconda.org/saska/trict/badges/latest_release_date.svg)](https://anaconda.org/saska/trict/)
[![Platforms](https://anaconda.org/saska/trict/badges/platforms.svg)](https://anaconda.org/saska/trict/)

# trict

Python dictionary with extra stuff.

Starting off, if you're seeing this, please give feedback! 

You can install with `pip install trict` or `conda install -c saska trict` (working on conda-forge). Doesn't currently have any dependencies (although you'll need `pytest` if you want to run the tests for some reason), only works with python>3.6 strictly because I like f-strings which I can reformat out if someone needs this to work on something else.

Tricktionaries (subclass of collections.UserDict) are dictionary-type things that have recursive (and other) helper things I've previously needed. Here's how they work:

You initialize a tricktionary with a normal dictionary.

```python
>>> from trict import Trict

>>> t = Trict({
    'user': {
        'information': {
            'attribute': 'infonugget',
            'another_attribute': 'secondnugget'
        },
        'moreinformation': 'extranugget'
    }
})
```
You can then perform all sorts of cool operations with it, like period-separated setting and getting (or any-string-separated, you can specify `key_sep` as a keyword argument in the Trict constructor, default is `.`).

```python
>>> t['user.information.attribute']
'infonugget'
```
Just like a python dictionary, Trict implements `get(key, default=None)` if you don't like KeyErrors.

When setting, the Trict will create intermediary keys for you:

```python
>>> t['user.newinformation.newattribute'] = 'new'
>>> t['user.newinformation.newattribute']
'new'
```

Deleting also works as you'd expect, so you can also `.pop()`. You can also do any of this using lists as keys.
```python
>>> key = ['user', 'information', 'another_attribute']
>>> t[key]
'secondnugget'
```

If you want to flatten your dictionary for a csv export for example (use keys as the header), you can do that. The constructor arg `key_sep` also affects how keys are formatted here. The Tricktionary can be rebuilt by passing this type of flattened dictionary into the alternate `from_flat_dict` constructor with the same `key_sep`.
```python
>>> t.flatten()
{
  'user.information.attribute': 'infonugget', 
  'user.information.another_attribute': 'secondnugget', 
  'user.moreinformation': 'extranugget', 
  'user.newinformation.newattribute': 'new'
}
```

Or do a complete traversal with `traverse`. It returns a generator yielding 2-tuples of (key-path, value).
```python
>>> for k, v in t.traverse():
...     print(f"{k}: {v}")
['user']: {'information': {'attribute': 'infonugget', 'another_attribute': 'secondnugget'}, 'moreinformation': 'extranugget', 'newinformation': {'newattribute': 'new'}}
['user', 'information']: {'attribute': 'infonugget', 'another_attribute': 'secondnugget'}
['user', 'information', 'attribute']: infonugget
['user', 'information', 'another_attribute']: secondnugget
['user', 'moreinformation']: extranugget
['user', 'newinformation']: {'newattribute': 'new'}
['user', 'newinformation', 'newattribute']: new
```
If you just need the leaves, you can do that as well with a similar format.
```python
>>> for k, v in t.leaves():
...     print(f"{k}: {v}")
['user', 'information', 'attribute']: infonugget
['user', 'information', 'another_attribute']: secondnugget
['user', 'moreinformation']: extranugget
['user', 'newinformation', 'newattribute']: new
```

You can also map the leaves (the actual values at the end of your dictionary) with a callable.
```python
>>> t.map_leaves(lambda x: x + " - and there's more!")
>>> t.data
{
  'user': {
    'information': {
      'attribute': "infonugget - and there's more!", 
      'another_attribute': "secondnugget - and there's more!"
    }, 
    'moreinformation': "extranugget - and there's more!", 
    'newinformation': {
      'newattribute': "new - and there's more!"
    }
  }
}
```

All the dictionary helper methods are also provided standalone. There's also an extra one, `iter_keys` that gives you a list of anything that's a key - helpful if there's a bunch of people writing in your codebase and you want to enforce say a regex naming convention on your keys or something.

If you're more of the "I need to make sure my API can handle most anything thrown at it!" type, you can define a mapper (using {new_key: [str or list]}, try and stick to one, it's prettier, example has both) and throw any dicts you receive into a Tricktionary and map them to the same format. Pretty handy if you need to take in documents in multiple formats, just make sure document x doesn't have different data from document y in the same key path.

```python
>>> mapper = {
        'newkey': [
            'user.noninformation.nonattribute', # Doesn't exist
            'user.information.another_attribute' # Finds
        ],
        'othernewkey': [
            ['user', 'noninformation'], # Doesn't exist
            ['user', 'information'] # Finds
        ]
    }
>>> t.map_with_dict(mapper)
{
  'newkey': "secondnugget - and there's more!", 
  'othernewkey': {
    'attribute': "infonugget - and there's more!", 
    'another_attribute': "secondnugget - and there's more!"
  }
}
```

Similar functionality can be found in `get_by_list` which also takes [str or list] and returns val if any of those keys exists.
