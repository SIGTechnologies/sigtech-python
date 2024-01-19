import datetime as dtm
from typing import Optional

import pandas as pd

from sigtech.api.client.utils import series_to_dict
from sigtech.api.framework.environment import env
from sigtech.api.framework.framework_api_object import FrameworkApiObject


class TradableTSIndex(FrameworkApiObject):
    """
    Tradable wrapper over a timeseries.

    :param currency: currency for initial cash and valuation
    :param timeseries: series or dataframe containing data points
    :param start_date: start date of the timeseries
    """

    def __init__(
        self,
        currency: str,
        timeseries: pd.Series,
        start_date: dtm.date,
    ):
        if not isinstance(currency, str):
            raise ValueError("currency must be str")
        if not isinstance(timeseries, pd.Series):
            raise ValueError("timeseries must be pandas Series")
        if not isinstance(start_date, dtm.date):
            raise ValueError("start_date must be date")
        self.currency = currency
        self.timeseries = timeseries
        assert (
            start_date == timeseries.index[0]
        ), "start_date must be the same as the first date in the timeseries"
        api_response = env().client.instruments.custom.create(
            session_id=env().session_id,
            currency=self.currency,
            timeseries=series_to_dict(self.timeseries),
        )
        super().__init__(api_response)
        self._history: Optional[pd.Series] = None

    def history(self) -> pd.Series:
        """
        History of TradableTimeseries.
        """
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
        self._history = ts.sort_index()
        return self._history
