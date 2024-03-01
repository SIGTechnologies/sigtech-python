from typing import List, Optional

import pandas as pd

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategies.strategy import Strategy


class ReinvestmentStrategy(Strategy):
    """
    ReinvestmentStrategy - Total return class for handling corporate actions for
    underlying stock/ETF.

    Note: 'get_single_stock_strategy' should be used for single stock
    ReinvestmentStrategy generation.

    Internally the strategy constructs holding periods of the underlyer based
    on the filter lists and expiry date setting of the underlyer.

    The building block schedules decisions for handling corporation actions
    throughout the lifetime of the strategy.

    :param underlyer: Identifier for underlying instrument.
    """

    def __init__(
        self,
        underlyer: str,
        _api_call: bool = False,  # used to prevent unsupported framework usage
    ):
        super().__init__(
            underlyer=underlyer,
            _api_call=_api_call,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch rolling future strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}

        ticker = api_inputs["underlyer"].upper().strip()
        assert (
            ticker.endswith("US EQUITY") and api_inputs["_api_call"]
        ) or ticker.endswith("UP EQUITY"), "The underlyer is not a supported ETF"

        api_inputs["identifier"] = ticker
        del api_inputs["underlyer"]
        del api_inputs["_api_call"]

        return env().client.instruments.stock.create(
            session_id=session_id,
            **api_inputs,
        )

    def history(self) -> pd.Series:
        """
        Returns the valuation history of the strategy
        (Not available for stocks and ETFs).
        """
        raise NotImplementedError("The total return history for stocks is restricted.")

    @property
    def currency(self) -> str:
        return self._get_reference_data()["currency"]


def get_single_stock_strategy(
    ticker: Optional[str] = None,
    exchange_ticker: Optional[str] = None,
    tickers: Optional[List[str]] = None,
    exchange_tickers: Optional[List[str]] = None,
):
    """
    Method used to generate a default reinvestment strategies for single stock or ETF.

    :param ticker: Tradable stock id, or list of tradable stock ids.
    :param exchange_ticker: Stock identifier, or list of stock identifier.
    :param tickers: List of ticker.
    :param exchange_tickers: List of exchange_ticker.

    :return: ``ReinvestmentStrategy`` object.
    """

    if exchange_tickers:
        return [
            ReinvestmentStrategy(underlyer=f"{u} US EQUITY", _api_call=True)
            for u in exchange_tickers
        ]
    elif tickers:
        return [ReinvestmentStrategy(underlyer=f"{u}", _api_call=True) for u in tickers]
    elif exchange_ticker:
        return ReinvestmentStrategy(
            underlyer=f"{exchange_ticker} US EQUITY", _api_call=True
        )
    elif ticker:
        return ReinvestmentStrategy(underlyer=f"{ticker}", _api_call=True)
    else:
        raise ValueError("A ticker or exchange ticker must be supplied.")
