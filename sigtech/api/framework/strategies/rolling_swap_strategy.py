import datetime as dtm
from typing import Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.client.utils import date_from_iso_format
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategies.strategy import Strategy


class RollingSwapStrategy(Strategy):
    """
    Strategy handling the rolling of forward starting IMM swaps.
    Swaps are receivers (receiving fixed, paying floating).
    """

    def __init__(
        self,
        tenor: str,
        currency: str,
        forward_start_months: int = 6,
        rolling_frequency_months: Optional[int] = None,
        start_date: Optional[Union[str, dtm.date]] = None,
    ):
        if not isinstance(tenor, str):
            raise ValueError("tenor must be str")
        if not isinstance(currency, str):
            raise ValueError("currency must be str")
        if not isinstance(forward_start_months, int):
            raise ValueError("forward_start_months must be int")
        if not isinstance(rolling_frequency_months, (type(None), int)):
            raise ValueError("rolling_frequency_months must be int")
        if not isinstance(start_date, (dtm.date, str, type(None))):
            raise ValueError("start_date must be date or str")
        rolling_frequency = None
        if rolling_frequency_months is not None:
            rolling_frequency = f"{rolling_frequency_months}M"
        forward_start = f"{forward_start_months}M"
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        super().__init__(
            currency=currency,
            tenor=tenor,
            forward_start=forward_start,
            rolling_frequency=rolling_frequency,
            start_date=(
                start_date.isoformat() if start_date is not None else start_date
            ),
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.swaps.rolling.create(
            session_id=session_id,
            **api_inputs,
        )

    @property
    def currency(self) -> str:
        return self._get_reference_data()["currency"]

    @property
    def tenor(self) -> str:
        return self._get_reference_data()["tenor"]

    @property
    def start_date(self) -> dtm.date:
        return date_from_iso_format(self._get_reference_data()["startDate"])

    @property
    def forward_start_months(self) -> int:
        forward_start = self._get_reference_data()["forwardStart"]
        assert forward_start.endswith("M")
        return int(forward_start[:-1])

    @property
    def rolling_frequency_months(self) -> int:
        rolling_frequency = self._get_reference_data()["rollingFrequency"]
        assert rolling_frequency.endswith("M")
        return int(rolling_frequency[:-1])

    @property
    def roll_offset(self) -> int:
        return self._get_reference_data()["rollOffset"]
