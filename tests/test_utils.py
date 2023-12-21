import datetime as dtm

import pytest

from sigtech.api.client.utils import (
    camel_to_snake,
    date_from_iso_format,
    singular,
    snake_to_camel,
)


@pytest.mark.parametrize(
    "name, expected",
    [
        ("camelCaseString", "camel_case_string"),
        ("myVariableName", "my_variable_name"),
        ("snake_case", "snake_case"),
    ],
)
def test_camel_to_snake(name, expected):
    assert camel_to_snake(name) == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("apples", "Apple"),
        ("status", "Status"),
        ("dogs", "Dog"),
    ],
)
def test_singular(name, expected):
    assert singular(name) == expected


@pytest.mark.parametrize(
    "name, expected",
    [
        ("snake_case_string", "snakeCaseString"),
        ("my_variable_name", "myVariableName"),
        ("camel_case", "camelCase"),
    ],
)
def test_snake_to_camel(name, expected):
    assert snake_to_camel(name) == expected


@pytest.mark.parametrize(
    "d, expected",
    [
        ("2000-01-01", dtm.date(2000, 1, 1)),
        ("2000-02-02", dtm.date(2000, 2, 2)),
        ("1999-12-12", dtm.date(1999, 12, 12)),
    ],
)
def test_date_from_iso_format(d, expected):
    assert date_from_iso_format(d) == expected


def test_date_from_iso_format_invalid():
    with pytest.raises(TypeError) as e:
        assert date_from_iso_format(22)
    assert e.value.args == ("argument must be str",)
    with pytest.raises(ValueError) as e:
        assert date_from_iso_format("asdf")
    assert e.value.args == ("Invalid isoformat string: 'asdf'",)
    with pytest.raises(ValueError) as e:
        assert date_from_iso_format("YYYY-MM-DD")
    assert e.value.args == ("Invalid isoformat string: 'YYYY-MM-DD'",)
