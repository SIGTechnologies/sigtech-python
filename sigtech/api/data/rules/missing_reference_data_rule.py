"""Code generated by __main__"""

from dataclasses import dataclass, field

from sigtech.api.data.utils import BaseRule


@dataclass
class MissingReferenceDataRule(BaseRule):
    """
    Check whether an expected value is missing from a static reference dataset.

    Example use case:
        As a data consumer, I want to make sure that for every bond I get a
        price for, I have a row available in my static data within 2 days
        of getting the first bond price.

    In the above example, the MissingReferenceDataRule must be configured on
    project 2, referencing the bond data in project 1, with a tolerance
    of 2 days.

    :param column (str): The column in the static reference dataset to check for missing values.
    :param project_to_map (str): Dynamic data used to validate the static reference data, e.g. bond prices.
    :param map_on (str): Column in the dynamic dataset which references the static reference data.
    :param tolerance_days (int): The number of days within which missing ref data are tolerated:
        - default: 0
        - min: 0

    docs: https://sigtech.gitbook.io/dave/rules#refdata
    """  # noqa: E501

    column: str = field(
        metadata={
            "description": (
                "The column in the static reference dataset to check for missing"
                " values."
            ),
            "type": "str",
        }
    )

    project_to_map: str = field(
        metadata={
            "description": (
                "Dynamic data used to validate the static reference data, e.g. bond"
                " prices."
            ),
            "type": "str",
        }
    )

    map_on: str = field(
        metadata={
            "description": (
                "Column in the dynamic dataset which references the static reference"
                " data."
            ),
            "type": "str",
        }
    )

    tolerance_days: int = field(
        metadata={
            "description": (
                "The number of days within which missing ref data are tolerated:"
            ),
            "default": 0,
            "min": 0,
            "type": "int",
        }
    )