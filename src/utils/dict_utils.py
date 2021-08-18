import json


def update_dictionaries(dict1: dict, dict2: dict):
    for key, value in dict2.items():
        if key not in dict1.keys():
            dict1[key] = []

        dict1[key].extend(value)


def stringify_dictionary(dict_obj: dict, indent: int = 2) -> str:
    result = json.dumps(
        {
            k: str(v)
            for k, v
            in dict_obj.items()
        },
        indent=indent)

    return result
