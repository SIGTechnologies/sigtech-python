from abc import ABC, abstractmethod
from typing import Optional

import pandas as pd

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env
from sigtech.api.framework.framework_api_object import FrameworkApiObject


class StrategyBase(FrameworkApiObject, ABC):
    """
    StrategyBase class.

    This is a base class for different strategy classes.
    """

    def __init__(self, **inputs) -> None:
        api_response = self._get_strategy_obj(env().session_id, **inputs)
        super().__init__(api_response)
        self._history: Optional[pd.Series] = None

    @abstractmethod
    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        This method is intended to be overridden in subclasses
        to fetch the strategy from the API.
        """
        raise NotImplementedError

    def history(self) -> pd.Series:
        """
        Returns the valuation history of the strategy.
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
