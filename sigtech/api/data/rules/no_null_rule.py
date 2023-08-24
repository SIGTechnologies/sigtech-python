"""Code generated by __main__"""

from dataclasses import dataclass, field
from typing import List

from sigtech.api.data.utils import BaseRule


@dataclass
class NoNullRule(BaseRule):
    """
    For the selected columns, raise an issue where a value in the column is null.

    :param columns (List[str]): Select at least one column:
        - minItems: 1
        - uniqueItems: True

    docs: https://sigtech.gitbook.io/dave/rules#null
    """  # noqa: E501

    columns: List[str] = field(
        metadata={
            "description": "Select at least one column:",
            "minItems": 1,
            "uniqueItems": True,
            "type": "List[str]",
        }
    )
