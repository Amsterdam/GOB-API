import re


def to_snake(camel: str):
    """
    Convert a camelCase string to snake

    Example:
        _to_snake(snakeCase) => snake_case

    :param camel:
    :return:
    """
    return re.sub('([A-Z])', r'_\1', camel).lower()


def to_camelcase(s):
    """Converts a snake_case string to camelCase

    Example:
        to_camelcase(snake_case) => snakeCase

    :param s: string to convert to camelCase
    :return:
    """
    def _camelcase_converter(m):
        return m.group(1).upper()

    _RE_TO_CAMELCASE = re.compile(r'(?!^)_([a-zA-Z])')
    return re.sub(_RE_TO_CAMELCASE, _camelcase_converter, s)


def dict_to_camelcase(d):
    """Converts a dict with snake_case key names to a dict with camelCase key names

    Recursive function to convert dictionaries with arbitrary depth to camelCase dictionaries

    Example:
        dict_to_camelcase({"snake_case": "value}) => {"snakeCase": "value}

    :param d:
    :return:
    """
    obj = {}
    for key, value in d.items():
        obj[to_camelcase(key)] = object_to_camelcase(value)
    return obj


def object_to_camelcase(value):
    """Converts an object with snake_case key names to an object with camelCase key names."""
    if isinstance(value, list):
        return [object_to_camelcase(v) for v in value]
    elif isinstance(value, dict):
        return dict_to_camelcase(value)
    else:
        return value