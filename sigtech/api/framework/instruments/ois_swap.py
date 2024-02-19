import datetime as dtm
from typing import Optional, Union

import pandas as pd

from sigtech.api import env
from sigtech.api.client.utils import date_from_iso_format
from sigtech.api.framework.instruments.base import Instrument


class OISSwap(Instrument):
    """
    OIS swap receiving fixed rate and paying OIS rate.

    Keyword arguments:

        * ``currency``: Currency of the swap.
        * ``tenor``: Tenor (e.g. ``5Y``)
        * ``fixed_rate``: Fixed rate (of the receiving leg).
                          Use the fair-rate on trade_date if None.
                          Expected in decimal format, e.g. 0.05 for 5%.
        * ``trade_date``: When the swap was agreed.
        * ``start_date``: Wen payments begin. Default is T+``settlement_days``.

    Example object creation:
        swap = OISSwap(
            currency='USD',
            tenor='1Y',
            trade_date='2019-07-01'
        )
    """

    def __init__(
        self,
        currency: str,
        tenor: str,
        trade_date: Union[dtm.date, str],
        start_date: Optional[Union[dtm.date, str]] = None,
        fixed_rate: Optional[float] = None,
    ):
        if not isinstance(currency, str):
            raise ValueError("currency must be str")
        if not isinstance(tenor, str):
            raise ValueError("tenor must be str")
        if not isinstance(trade_date, (dtm.date, str)):
            raise ValueError("trade_date must be date or str")
        if not isinstance(start_date, (dtm.date, str, type(None))):
            raise ValueError("start_date must be date or str")
        if not isinstance(fixed_rate, (float, type(None))):
            raise ValueError("fixed_rate must be float or None")

        if isinstance(trade_date, str):
            trade_date = date_from_iso_format(trade_date)
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        self._currency = currency
        self._tenor = tenor
        self._trade_date = trade_date
        self._start_date = start_date
        self._fixed_rate = fixed_rate
        self._data_df: Optional[pd.DataFrame] = None
        api_response = env().client.instruments.otc.overnight_index_swap.create(
            session_id=env().session_id,
            currency=self._currency,
            tenor=self._tenor,
            trade_date=(
                self._trade_date.isoformat()
                if isinstance(self._trade_date, dtm.date)
                else self._trade_date
            ),
            start_date=(
                self._start_date.isoformat()
                if isinstance(self._start_date, dtm.date)
                else self._start_date
            ),
            fixed_rate=self._fixed_rate,
        )
        super().__init__(api_response)

    @property
    def currency(self):
        return self._currency

    @property
    def tenor(self) -> str:
        return self._tenor

    @property
    def trade_date(self) -> dtm.date:
        return self._trade_date

    @property
    def start_date(self) -> dtm.date:
        return self._start_date or date_from_iso_format(
            self._get_reference_data()["startDate"]
        )

    @property
    def maturity(self) -> dtm.date:
        return date_from_iso_format(self._get_reference_data()["maturityDate"])

    @property
    def fixed_rate(self) -> float:
        if self._fixed_rate is not None:
            return self._fixed_rate
        return self._get_reference_data()["fixedRate"]

    @property
    def fixing_lag(self) -> int:
        return self._get_reference_data()["fixingLag"]

    @property
    def pay_delay(self) -> int:
        return self._get_reference_data()["payDelay"]

    @property
    def settlement_days(self) -> int:
        return self._get_reference_data()["settlementDays"]

    @property
    def day_count(self) -> str:
        return self._get_reference_data()["dayCount"]

    @property
    def frequency(self) -> str:
        return self._get_reference_data()["frequency"]

    @property
    def index(self) -> str:
        return self._get_reference_data()["index"]

    def data_df(self) -> pd.DataFrame:
        if self._data_df is not None:
            return self._data_df
        self.creation_response.wait_for_object_status()
        api_response = env().client.data.history.get(
            session_id=env().session_id,
            object_id=self.api_object_id,
        )
        data_df = pd.DataFrame(api_response.history).rename(
            columns={
                "$timestamp": "trading_datetime",
                "$history": "LastPrice",
                "fairRate": "FairRate",
                "pv01": "PV01",
            }
        )
        data_df = data_df.set_index("trading_datetime")
        data_df.index = pd.to_datetime(data_df.index)
        self._data_df = data_df
        assert isinstance(self._data_df, pd.DataFrame)
        return self._data_df

    def history(self) -> pd.Series:
        data_df = self.data_df()
        ts = data_df["LastPrice"].copy()
        ts.index.name = None
        ts = ts.rename(self.name)
        return ts
