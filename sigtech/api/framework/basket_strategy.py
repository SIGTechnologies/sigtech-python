import datetime as dtm

from sigtech.api.framework.environment import env, obj
from sigtech.api.framework.strategy_base import StrategyBase


class BasketStrategy(StrategyBase):

    def __init__(self, constituent_names, weights, currency=None, rebalance_frequency='EOM', start_date=None):
        constituents = [obj.get(x) if isinstance(x, str) else x for x in constituent_names]
        for fapi_obj in constituents:
            fapi_obj.entity.wait_for_object_status()
        constituent_ids = [x.api_object_id for x in constituents]
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(constituents=constituent_ids, weights=weights, currency=currency,
                         rebalance_frequency=rebalance_frequency, start_date=start_date)

    def _get_strategy_fa_obj(self, session_id, **inputs):
        api_inputs = inputs.copy()
        for input_key in inputs:
            if inputs[input_key] is None:
                del api_inputs[input_key]

        return env().client.strategies.basket.create(
            session_id=session_id, **api_inputs
        )
