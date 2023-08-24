"""Code generated by __main__"""

from dataclasses import dataclass, field
from typing import List

from sigtech.api.data.utils import BaseRule


@dataclass
class LeadingZerosRule(BaseRule):
    """
    For the selected columns, raise an issue if the value in the first row(s) is zero.

    :param columns (List[str]): Select at least one column:
        - minItems: 1
        - uniqueItems: True

    docs: https://sigtech.gitbook.io/dave/rules#zeros
    """  # noqa: E501

    columns: List[str] = field(
        metadata={
            "description": "Select at least one column:",
            "minItems": 1,
            "uniqueItems": True,
            "type": "List[str]",
        }
    )
