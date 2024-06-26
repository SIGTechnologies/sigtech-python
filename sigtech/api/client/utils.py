import datetime as dtm
import math
import re

import numpy as np
import pandas as pd


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


def date_from_iso_format(s: str) -> dtm.date:
    # Parse dates in ISO-8601 form. e.g. "2000-01-01"
    # python3.6 and below do not have date.fromisoformat()
    if not isinstance(s, str):
        raise TypeError("argument must be str")
    if not (len(s) == 10 and s[4] == "-" and s[7] == "-"):
        raise ValueError(f"Invalid isoformat string: {repr(s)}")
    try:
        year, month, day = int(s[0:4]), int(s[5:7]), int(s[8:10])
    except ValueError:
        raise ValueError(f"Invalid isoformat string: {repr(s)}")
    return dtm.date(year, month, day)


def removesuffix(s: str, suffix: str) -> str:
    # python3.8 and below do not have str.removesuffix()
    if len(suffix) > 0 and s.endswith(suffix):
        return s[: -len(suffix)]
    return s


def series_to_dict(s: pd.Series) -> dict:
    timestamps = np.datetime_as_string(
        s.index.values,
        unit="auto",
    )
    return {
        "$timestamp": timestamps.tolist(),
        "$history": [o if math.isfinite(o) else None for o in s.values.tolist()],
    }
