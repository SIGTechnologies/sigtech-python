import datetime as dtm
from typing import List, Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env, obj
from sigtech.api.framework.framework_api_object import FrameworkApiObject
from sigtech.api.framework.strategy_base import StrategyBase


class BasketStrategy(StrategyBase):
    """
    BasketStrategy class implements a long-only basket strategy with fixed weights,
    rebalanced as per the rebalance frequency.

    :param constituent_names: List of constituent tickers.
    :param weights: List of constituents weights expressed as floats.
    :param currency: Base strategy currency for initial cash and valuation.
        Defaults to 'USD'.
    :param rebalance_frequency: Rebalance frequency. For example: '1BD', '2BD', '1W',
        '2W', '1M', '2M', '1W-WED', '1W-FRI', '3M_IMM', 'SOM', 'EOM', 'YEARLY', '1DOM',
        and variations of these. Defaults to 'EOM'.
    :param start_date: Start of strategy. Optional.
    """

    def __init__(
        self,
        constituent_names: List[Union[str, FrameworkApiObject]],
        weights: List[float],
        currency: Optional[str] = "USD",
        rebalance_frequency: str = "EOM",
        start_date: Optional[Union[str, dtm.date]] = None,
    ):
        constituents: List[FrameworkApiObject] = [
            obj.get(x) if isinstance(x, str) else x for x in constituent_names
        ]
        for fapi_obj in constituents:
            fapi_obj.creation_response.wait_for_object_status()
        constituent_ids = [x.api_object_id for x in constituents]
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(
            constituents=constituent_ids,
            weights=weights,
            currency=currency,
            rebalance_frequency=rebalance_frequency,
            start_date=start_date,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch basket strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.basket.create(
            session_id=session_id, **api_inputs
        )
