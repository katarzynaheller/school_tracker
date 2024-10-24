def get_values_from_dict(dictionary: dict, keys: list) -> dict:
    """
    Retrieve dictionary values from a list of keys.

    :param dictionary: The dictionary to retrieve values from.
    :param keys: The list of keys to look for in the dictionary.
    :return: A list of values corresponding to the keys.
    """
    return {key: value for key, value in dictionary.items() if key in keys}