from dataclasses import Field, dataclass, fields


@dataclass
class BaseRule:
    """Base class used to validate rule inputs given constraints."""

    def __post_init__(self):
        self._validate_fields()

    def _validate_fields(self):
        for field in fields(self):
            if field.type in (int, float):
                self._validate_min_max(field)
            if field.type is list:
                self._validate_list(field)

    def _validate_list(self, field: Field):
        value = getattr(self, field.name)
        assert isinstance(value, list)
        min_items = field.metadata.get("minItems")
        assert isinstance(min_items, int)

        if len(value) < min_items:
            raise ValueError(f"{field.name} must have at least {min_items} items")

    def _validate_min_max(self, field: Field):
        value = getattr(self, field.name)
        min_value = field.metadata.get("min")
        max_value = field.metadata.get("max")

        if min_value is not None and value < min_value:
            raise ValueError(
                f"{field.name} must be greater than or equal to {min_value}"
            )

        if max_value is not None and value > max_value:
            raise ValueError(f"{field.name} must be less than or equal to {max_value}")
