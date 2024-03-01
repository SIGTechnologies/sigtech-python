import datetime as dtm
from typing import Optional, Union

import pandas as pd

from sigtech.api import env
from sigtech.api.client.utils import date_from_iso_format
from sigtech.api.framework.instruments.base import Instrument


class FXForward(Instrument):
    """
    FX Forward Instrument to exchange two currencies at a future payment date.
    """

    def __init__(
        self,
        over: str,
        under: str,
        payment_date: Union[dtm.date, str],
        start_date: Union[dtm.date, str],
        strike: Optional[float] = None,
    ):
        if not isinstance(over, str):
            raise ValueError("over must be str")
        if not isinstance(under, str):
            raise ValueError("under must be str")
        if not isinstance(payment_date, (dtm.date, str)):
            raise ValueError("trade_date must be date or str")
        if not isinstance(start_date, (dtm.date, str, type(None))):
            raise ValueError("start_date must be date or str")
        if not isinstance(strike, (float, type(None))):
            raise ValueError("strike must be float or None")

        if isinstance(payment_date, str):
            payment_date = date_from_iso_format(payment_date)
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        self._over = over
        self._under = under
        self._payment_date = payment_date
        self._start_date = start_date
        self._strike = strike
        self._history: Optional[pd.Series] = None
        api_response = env().client.instruments.otc.fx_forward.create(
            session_id=env().session_id,
            quote_currency=self._over,
            base_currency=self._under,
            payment_date=self._payment_date.isoformat(),
            start_date=self._start_date.isoformat(),
            forward_rate=self._strike,
        )
        super().__init__(api_response)

    @property
    def over(self):
        return self._over

    @property
    def under(self) -> str:
        return self._under

    @property
    def payment_date(self) -> dtm.date:
        return self._payment_date

    @property
    def start_date(self) -> dtm.date:
        return self._start_date

    @property
    def strike(self) -> float:
        if self._strike is not None:
            return self._strike
        return self._get_reference_data()["forwardRate"]

    def history(self) -> pd.Series:
        if self._history is not None:
            return self._history
        self.creation_response.wait_for_object_status()
        api_response = env().client.performance.history.get(
            session_id=env().session_id,
            object_id=self.api_object_id,
        )
        df = pd.DataFrame(api_response.history).rename(
            {"$timestamp": "date", "$history": "history"}, axis=1
        )
        ts = df.set_index("date")["history"].rename(self.name)
        ts.index = pd.to_datetime(ts.index)
        ts.index.name = None
        self._history = ts.sort_index()
        return self._history
