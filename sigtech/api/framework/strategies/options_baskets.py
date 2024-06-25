import datetime as dtm
from typing import List, Literal, Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.client.utils import date_from_iso_format, removesuffix
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategies.strategy import Strategy


class StraddleOptionStrategy(Strategy):
    """
    A strategy that takes the same position in both a
    call option and a put option with the same expiration
    and strike price.

    This generally profits if the stock price increase or decrease,
    or if volatility increases.

    Example usage:

    ::

        import datetime as dtm
        import sigtech.framework as sig

        group = sig.obj.get('SPX INDEX OTC OPTION GROUP')
        straddle = sig.StraddleOptionStrategy(
            start_date=dtm.date(2021, 1, 4),
            end_date=dtm.date(2023, 1, 4),
            currency=group.underlying_obj.currency,
            group_name=group.name,
            maturity='3M',
            strike_type='Delta',
            strike=0.5
        )

    """

    def __init__(
        self,
        group_name: str,
        start_date: Union[dtm.date, str],
        maturity: Union[dtm.date, str],
        strike: Optional[float] = None,
        strike_type: Literal["SPOT", "Delta", "Price", "Premium"] = "Price",
        exercise_type: Literal["European", "American"] = "European",
        currency: Optional[str] = None,
    ):
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        if isinstance(maturity, str):
            maturity = date_from_iso_format(maturity)

        if not group_name.endswith(" OTC OPTION GROUP"):
            raise ValueError("group_name have ' OTC OPTION GROUP' suffix")

        underlying = removesuffix(group_name, " OTC OPTION GROUP")
        if not underlying.endswith(" INDEX"):
            underlying = f"{underlying} CURNCY"

        if exercise_type not in ("European", "American"):
            raise ValueError("exercise_type must be 'European' or 'American'")

        self._underlying = underlying
        self._start_date = start_date
        self._maturity = maturity
        self._exercise_type = exercise_type

        _strike: Optional[Union[str, float]] = strike
        if strike_type == "SPOT":
            _strike, strike_type = "SPOT", "Price"
        super().__init__(
            strike=_strike,
            strike_type=strike_type.upper(),
            exercise_style=exercise_type.upper(),
            start_date=start_date.isoformat(),
            maturity=maturity.isoformat(),
            identifier=f"{underlying}",
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.otc.options.straddle.create(
            session_id=session_id,
            **api_inputs,
        )


class RollingStraddleOptionStrategy(Strategy):
    """
    A strategy that takes the same position in both a
    call option and a put option with the same expiration
    and strike price.

    This generally profits if the stock price increase or decrease,
    or if volatility increases.

    Example usage:

    ::

        import datetime as dtm
        import sigtech.framework as sig

        group = sig.obj.get('SPX INDEX OTC OPTION GROUP')
        straddle = sig.StraddleOptionStrategy(
            start_date=dtm.date(2021, 1, 4),
            end_date=dtm.date(2023, 1, 4),
            currency=group.underlying_obj.currency,
            group_name=group.name,
            maturity='3M',
            strike_type='Delta',
            strike=0.5
        )

    """

    def __init__(
        self,
        group_name: str,
        start_date: Union[dtm.date, str],
        rolling_frequencies: List[str],
        maturity: Literal["1M"],
        strike: Optional[float] = None,
        strike_type: Literal["SPOT", "Delta", "Price", "Premium"] = "Price",
        exercise_type: Literal["European", "American"] = "European",
        currency: Optional[str] = None,
    ):
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        if not isinstance(maturity, str):
            raise ValueError("maturity must be str")

        if not group_name.endswith(" OTC OPTION GROUP"):
            raise ValueError("group_name have ' OTC OPTION GROUP' suffix")
        underlying = removesuffix(group_name, " OTC OPTION GROUP")
        if not underlying.endswith(" INDEX"):
            underlying = f"{underlying} CURNCY"

        if exercise_type not in ("European", "American"):
            raise ValueError("exercise_type must be 'European' or 'American'")

        if not isinstance(rolling_frequencies, list):
            raise ValueError("rolling_frequencies must be a list")
        if len(rolling_frequencies) != 1:
            raise ValueError("only 1 rolling frequency is supported")

        self._underlying = underlying
        self._start_date = start_date
        self._maturity = maturity
        self._exercise_type = exercise_type

        _strike: Optional[Union[str, float]] = strike
        if strike_type == "SPOT":
            _strike, strike_type = "SPOT", "Price"
        super().__init__(
            strike=_strike,
            strike_type=strike_type.upper(),
            exercise_style=exercise_type.upper(),
            start_date=start_date.isoformat(),
            tenor=maturity,
            identifier=f"{underlying}",
            rolling_frequency=rolling_frequencies[0],
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        return env().client.strategies.otc.options.rolling_straddle.create(
            session_id=session_id,
            **api_inputs,
        )
