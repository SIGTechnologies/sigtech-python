import datetime as dtm
from typing import Optional, Union

import pandas as pd

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env, obj
from sigtech.api.framework.strategy_base import StrategyBase


class SignalStrategy(StrategyBase):
    """
    SignalStrategy class implements a basket of instruments that change through time
    based on a signal.

    :param signal_input: DataFrame of weights through time.
    :param currency: Base strategy currency for initial cash and valuation,
                    (optional) defaults to 'USD'.
    :param rebalance_frequency: Rebalance frequency. For example: '1BD', '2BD', '1W',
                            '2W', '1M', '2M', '1W-WED', '1W-FRI', '3M_IMM', 'SOM',
                            'EOM', 'YEARLY', '1DOM', and variations of these,
                            (optional) defaults to 'EOM'.
    :param start_date: Start of strategy (optional).
    """

    def __init__(
        self,
        signal_input: pd.DataFrame,
        currency: Optional[str] = "USD",
        rebalance_frequency: str = "EOM",
        start_date: Optional[Union[str, dtm.date]] = None,
    ):
        signal_input = signal_input.copy()
        constituents = [obj.get(x) for x in signal_input.columns]
        for fapi_obj in constituents:
            fapi_obj.creation_response.wait_for_object_status()
        signal_input.columns = pd.Index([x.api_object_id for x in constituents])
        assert isinstance(signal_input.index, pd.DatetimeIndex)
        signal_input.index = signal_input.index.strftime("%Y-%m-%dT%H:%M:%S")
        signal_input.index.name = "$timestamp"
        signal_input_json = signal_input.reset_index().to_dict(orient="list")
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(
            signal=signal_input_json,
            currency=currency,
            rebalance_frequency=rebalance_frequency,
            start_date=start_date,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch signal strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.signal.create(
            session_id=session_id, **api_inputs
        )
