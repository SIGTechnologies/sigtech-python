import re


class SigApiException(Exception):
    pass


def camel_to_snake(name: str) -> str:
    """
    Converts a camelCase string to snake_case.

    :param name: The camelCase string to convert.
    :return: The snake_case version of the input string.
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", name).lower()


def singular(name: str) -> str:
    """
    Converts a word to its singular form.

    :param name: The word to convert.
    :return: The singular form of the input word.
    """
    if name == "status":
        pass
    elif name.endswith("s"):
        name = name[:-1]
    return name.title()


def snake_to_camel(name: str) -> str:
    """
    Converts a snake_case string to camelCase.

    :param name: The snake_case string to convert.
    :return: The camelCase version of the input string.
    """
    words = [word.title() for word in name.split("_")]
    words[0] = words[0].lower()
    return "".join(words)
