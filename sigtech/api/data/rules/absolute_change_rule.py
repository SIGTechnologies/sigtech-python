"""Code generated by __main__"""

from dataclasses import dataclass, field
from typing import List

from sigtech.api.data.utils import BaseRule


@dataclass
class AbsoluteChangeRule(BaseRule):
    """
    For the selected columns, raise an issue where the absolute change between consecutive data points is greater than the set limit.

    :param columns (List[str]): Select at least one column:
        - minItems: 1
        - uniqueItems: True
    :param threshold (float): Raise an issue for an absolute change greater than
        - default: 100.0
        - min: 0.0

    docs: https://sigtech.gitbook.io/dave/rules#absolute
    """  # noqa: E501

    columns: List[str] = field(
        metadata={
            "description": "Select at least one column:",
            "minItems": 1,
            "uniqueItems": True,
            "type": "List[str]",
        }
    )

    threshold: float = field(
        default=100.0,
        metadata={
            "description": "Raise an issue for an absolute change greater than",
            "default": 100.0,
            "min": 0.0,
            "type": "float",
        },
    )