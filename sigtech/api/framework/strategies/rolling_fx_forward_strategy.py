import datetime as dtm
from typing import Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.client.utils import date_from_iso_format
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategies.strategy import Strategy


class RollingFXForwardStrategy(Strategy):
    """
    Strategy that regularly rolls FX forwards.
    """

    def __init__(
        self,
        currency: str,
        long_currency: str,
        forward_tenor: str,
        start_date: Optional[Union[str, dtm.date]] = None,
    ):
        if not isinstance(currency, str):
            raise ValueError("currency must be str")
        if not isinstance(long_currency, str):
            raise ValueError("long_currency must be str")
        if not isinstance(forward_tenor, str):
            raise ValueError("forward_tenor must be str")
        if not isinstance(start_date, (dtm.date, str, type(None))):
            raise ValueError("start_date must be date or str")
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        super().__init__(
            quote_currency=currency,
            base_currency=long_currency,
            tenor=forward_tenor,
            start_date=(
                start_date.isoformat() if start_date is not None else start_date
            ),
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.fx_forwards.rolling.create(
            session_id=session_id,
            **api_inputs,
        )

    @property
    def currency(self) -> str:
        return self._get_reference_data()["quoteCurrency"]

    @property
    def long_currency(self) -> str:
        return self._get_reference_data()["baseCurrency"]

    @property
    def forward_tenor(self) -> str:
        return self._get_reference_data()["tenor"]

    @property
    def start_date(self) -> dtm.date:
        return date_from_iso_format(self._get_reference_data().get("startDate"))
