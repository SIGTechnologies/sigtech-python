import datetime as dtm
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategy_base import StrategyBase


class RollingFutureStrategy(StrategyBase):

    def __init__(self, contract_code, contract_sector, currency=None, rolling_rule=None, front_offset=None,
                 start_date=None, monthly_roll_days=None):
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(contract_code=contract_code, contract_sector=contract_sector, currency=currency,
                         rolling_rule=rolling_rule, front_offset=front_offset, start_date=start_date,
                         monthly_roll_days=monthly_roll_days)

    def _get_strategy_fa_obj(self, session_id, **inputs):
        api_inputs = inputs.copy()
        api_inputs['identifier'] = api_inputs['contract_code'] + ' ' + api_inputs['contract_sector']
        del api_inputs['contract_code']
        del api_inputs['contract_sector']
        for input_key in inputs:
            if inputs[input_key] is None:
                del api_inputs[input_key]

        return env().client.strategies.futures.rolling.create(
            session_id=session_id, **api_inputs,
        )
