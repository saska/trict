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

def invalid_base_dict():
    return {
        'user': {
            'information': {
                'attr.ibute': 'infonugget',
                'another_attribute': 'secondnugget'
            },
            'moreinformation': 'extranugget'
        }
    }