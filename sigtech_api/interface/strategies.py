from sigtech_api.interface.api_object import FrameworkApiObject, obj, Environment
import pandas as pd
import datetime as dtm


class Strategy(FrameworkApiObject):

    def __init__(self, **inputs):
        api_response = self._get_strategy_fa_obj(Environment.GLOBAL_SESSION, **inputs)
        super().__init__(api_response)
        self._history = None

    def _get_strategy_fa_obj(self, session_id, **inputs):
        return None

    def input_parameters(self):
        return ''

    def history(self):
        if self._history is not None:
            return self._history

        self.entity.wait()
        api_response = Environment.API.data.history.get(
            session_id=Environment.GLOBAL_SESSION,
            object_id=self.object_id,
        )
        ts = pd.Series(api_response.history)
        ts.index = pd.to_datetime(ts.index)
        self._history = ts.sort_index()
        return self._history


class RollingFutureStrategy(Strategy):

    def __init__(self, contract_code, contract_sector, currency=None, rolling_rule=None, front_offset=None,
                 start_date=None, monthly_roll_days='1:5'):
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(contract_code=contract_code, contract_sector=contract_sector, currency=currency,
                         rolling_rule=rolling_rule, front_offset=front_offset, start_date=start_date,
                         monthly_roll_days=monthly_roll_days)

    def _get_strategy_fa_obj(self, session_id, **inputs):
        return Environment.API.strategies.futures.rolling.create(
            session_id=session_id,
            currency=inputs['currency'],
            identifier=inputs['contract_code'] + ' ' + inputs['contract_sector'],
            rolling_rule=inputs['rolling_rule'],
            front_offset=inputs['front_offset'],
            start_date=inputs['start_date'],
            monthly_roll_days=inputs['monthly_roll_days'],
        )


class BasketStrategy(Strategy):

    def __init__(self, constituent_names, weights, currency=None, rebalance_frequency='1BD', start_date=None):
        constituents = [obj.get(x) if isinstance(x, str) else x for x in constituent_names]
        for fapi_obj in constituents:
            fapi_obj.entity.wait()
        constituent_ids = [x.object_id for x in constituents]
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(constituents=constituent_ids, weights=weights, currency=currency,
                         rebalance_frequency=rebalance_frequency, start_date=start_date)

    def _get_strategy_fa_obj(self, session_id, **inputs):
        return Environment.API.strategies.basket.create(
            session_id=session_id,
            currency=inputs['currency'],
            constituents=inputs['constituents'],
            weights=inputs['weights'],
            rebalance_frequency=inputs['rebalance_frequency'],
            start_date=inputs['start_date'],
        )
