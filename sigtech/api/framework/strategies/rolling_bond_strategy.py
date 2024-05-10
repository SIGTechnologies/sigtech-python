import datetime as dtm
from typing import Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategies.strategy import Strategy


class SingleBondStrategy(Strategy):
    """
    Strategy assigning weight to a single bond instrument and reinvesting bond coupons.

    Keyword arguments:

        * ``bond_name``: Name of bond to trade.

    """

    def __init__(
        self,
        bond_name: str,
        currency: Optional[str] = None,  # QUANT-1537
    ):
        super().__init__(
            currency=currency,
            bond_name=bond_name,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch rolling bond strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        api_inputs["identifier"] = api_inputs.pop("bond_name")
        del api_inputs["currency"]
        return env().client.strategies.bonds.reinvestment.create(
            session_id=session_id,
            **api_inputs,
        )

    @property
    def currency(self) -> str:
        return self._get_reference_data()["currency"]

    @property
    def start_date(self) -> str:
        return self._get_reference_data()["startDate"]


class RollingBondStrategy(Strategy):
    """
    Rolling bond strategy that rolls bonds.
    Invests in the underlying bonds using SingleBondStrategy, coupons are reinvested.

    Keyword arguments:

        * ``country``: Two-letter country code, e.g. ``'US'`` or ``'GB'``.
        * ``tenor``: Tenor string in ``'[xx]Y'`` format, e.g. ``'10Y'`` or ``'5Y'``.
        * ``start_date``: Start date of the strategy.
    """

    def __init__(
        self,
        country: str,
        tenor: str,
        start_date: Optional[Union[str, dtm.date]] = None,
    ):
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(
            country=country,
            tenor=tenor,
            start_date=start_date,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch rolling bond strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.bonds.rolling.create(
            session_id=session_id,
            **api_inputs,
        )

    @property
    def currency(self) -> str:
        return self._get_reference_data()["currency"]

    @property
    def tenor(self) -> str:
        return self._get_reference_data()["tenor"]

    @property
    def country(self) -> str:
        return self._get_reference_data()["country"]

    @property
    def start_date(self) -> str:
        return self._get_reference_data()["startDate"]
