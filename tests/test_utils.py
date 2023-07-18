import pytest

from sigtech.api.client.utils import camel_to_snake, singular, snake_to_camel


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
