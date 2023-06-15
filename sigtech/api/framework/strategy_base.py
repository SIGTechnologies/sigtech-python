from sigtech.api.framework.environment import env
from sigtech.api.framework.framework_api_object import FrameworkApiObject
import pandas as pd


class StrategyBase(FrameworkApiObject):
    """
    StrategyBase class.

    This is a base class for different strategy classes.
    """
    def __init__(self, **inputs):
        api_response = self._get_strategy_obj(env().session_id, **inputs)
        super().__init__(api_response)
        self._history = None

    def _get_strategy_obj(self, session_id: str, **inputs) -> None:
        """
        This method is intended to be overridden in subclasses to fetch the strategy from the API.
        """
        raise NotImplementedError

    def history(self) -> pd.Series:
        """
        Returns the valuation history of the strategy.
        """
        if self._history is not None:
            return self._history

        self.creation_response.wait_for_object_status()
        api_response = env().client.data.history.get(
            session_id=env().session_id,
            object_id=self.api_object_id,
        )
        ts = pd.Series(api_response.history, name=self.name)
        ts.index = pd.to_datetime(ts.index)
        ts.index = ts.index.tz_convert('UTC').tz_localize(None)
        self._history = ts.sort_index()
        return self._history
