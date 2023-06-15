from sigtech.api.framework.environment import env
from sigtech.api.framework.framework_api_object import FrameworkApiObject
import pandas as pd


class StrategyBase(FrameworkApiObject):

    def __init__(self, **inputs):
        api_response = self._get_strategy_fa_obj(env().session_id, **inputs)
        super().__init__(api_response)
        self._history = None

    def _get_strategy_fa_obj(self, session_id, **inputs):
        return None

    def input_parameters(self):
        return ''

    def history(self):
        if self._history is not None:
            return self._history

        self.entity.wait_for_object_status()
        api_response = env().client.data.history.get(
            session_id=env().session_id,
            object_id=self.api_object_id,
        )
        ts = pd.Series(api_response.history)
        ts.index = pd.to_datetime(ts.index)
        ts.index = ts.index.tz_convert('UTC').tz_localize(None)
        self._history = ts.sort_index()
        return self._history
