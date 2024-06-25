import datetime as dtm
import re
from typing import Literal, Optional, Union

import pandas as pd

from sigtech.api import env
from sigtech.api.client.utils import date_from_iso_format
from sigtech.api.framework.instruments.base import Instrument


class EquityIndexOTCOption(Instrument):
    """
    A class implementing OTC equity index option instruments.

        * ``underlying``: Underlying index of the option (e.g. ``SPX INDEX``)
        * ``start_date``: Option start date.
        * ``strike``: Strike price of the option.
        * ``maturity_date``: Maturity date of the option.
        * ``option_type``: Type of the option, either ``'Call'`` or ``'Put'``.
        * ``exercise_type``: Exercise style: ``'European'`` or ``'American'``.


    Example creation:
    ::

        equity_index_option = sig.EquityIndexOTCOption(
            start_date=dtm.date(2018, 1, 2),
            strike=2600,
            maturity_date=dtm.date(2018, 3, 23),
            option_type='Call',
            exercise_type='European',
            underlying='SPX INDEX'
        )

    """

    def __init__(
        self,
        underlying: str,
        strike: Union[float, str],
        start_date: Union[dtm.date, str],
        maturity_date: Union[dtm.date, str],
        option_type: Literal["Put", "Call"],
        strike_type: Literal["Price", "Delta", "Premium"] = "Price",
        exercise_type: Literal["European", "American"] = "European",
        currency: Optional[str] = None,
    ):
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        if isinstance(maturity_date, str):
            maturity_date = date_from_iso_format(maturity_date)
        if not isinstance(underlying, str):
            raise ValueError("underlying must be str")
        if option_type not in ("Call", "Put"):
            raise ValueError("option_type must be 'Call' or 'Put'")
        if exercise_type not in ("European", "American"):
            raise ValueError("exercise_type must be 'European' or 'American'")
        if not (
            isinstance(strike, (float, int))
            or (
                isinstance(strike, str)
                and re.match(r"^(SPOT|FWD)([+-]\d{1,2}%)?$", strike)
            )
        ):
            raise ValueError(
                "strike must be a number or string like: "
                "'SPOT', 'FWD', 'SPOT+10%', 'FWD-5%'"
            )
        if isinstance(strike, str) and "FWD" in strike:
            strike = strike.replace("FWD", "FORWARD")
        self._underlying = underlying
        self._start_date = start_date
        self._maturity_date = maturity_date
        self._option_type = option_type
        self._exercise_type = exercise_type
        api_response = env().client.instruments.otc.equity_index_option.create(
            session_id=env().session_id,
            strike=strike,
            strike_type=strike_type.upper(),
            type=option_type.upper(),
            exercise_style=exercise_type.upper(),
            start_date=start_date.isoformat(),
            maturity=maturity_date.isoformat(),
            identifier=f"{underlying}",
        )
        self._metrics: Optional[pd.DataFrame] = None
        super().__init__(api_response)

    @property
    def underlying(self) -> str:
        return self._underlying

    @property
    def strike(self) -> float:
        return self._get_reference_data()["strike"]

    @property
    def start_date(self) -> dtm.date:
        return self._start_date

    @property
    def maturity_date(self) -> dtm.date:
        return self._maturity_date

    @property
    def option_type(self) -> str:
        return self._option_type

    @property
    def exercise_type(self) -> str:
        return self._exercise_type

    def metrics(self) -> pd.DataFrame:
        if self._metrics is not None:
            return self._metrics

        self.creation_response.wait_for_object_status()
        api_response = env().client.data.history.get(
            session_id=env().session_id,
            object_id=self.api_object_id,
        )

        metrics_df = pd.DataFrame(api_response.history).rename(
            columns={
                "$timestamp": "trading_datetime",
                "$history": "NPV",
                "delta": "Delta",
                "gamma": "Gamma",
                "theta": "Theta",
                "vega": "Vega",
                "impliedVolatility": "ImpliedVolatility",
                "premiumAdjustedDelta": "PA Delta",
            }
        )
        metrics_df = metrics_df.set_index("trading_datetime")
        metrics_df.index = pd.to_datetime(metrics_df.index)
        self._metrics = metrics_df
        assert isinstance(self._metrics, pd.DataFrame)
        return self._metrics

    def data_df(self) -> pd.DataFrame:
        return self.metrics()[["NPV", "ImpliedVolatility"]]

    def history(self) -> pd.Series:
        return self.metrics()["NPV"]


class FXOTCOption(Instrument):
    """
    A class implementing OTC FX option instruments.
        * ``under``: Under currency of the underlying pair
                     (e.g. ``EUR`` for ``EURUSD``).
        * ``over``: Over currency of the underlying pair
                     (e.g. ``USD`` for ``EURUSD``).
        * ``start_date``: Option start date.
        * ``strike``: Strike price of the option.
        * ``maturity_date``: Maturity date of the option.
        * ``option_type``: Type of the option, either ``'Call'`` or ``'Put'``.
        * ``exercise_type``: Exercise style: ``'European'`` or ``'American'``.


    Example creation:
    ::
        fx_option = sig.FXOTCOption(
            over='USD',
            under='EUR',
            strike=1.0635,
            start_date=dtm.date(2017, 1, 6),
            maturity_date=dtm.date(2017, 4, 6),
            option_type='Call'
        )

    """

    def __init__(
        self,
        over: str,
        under: str,
        strike: Union[float, str],
        start_date: Union[dtm.date, str],
        maturity_date: Union[dtm.date, str],
        option_type: Literal["Put", "Call"],
        strike_type: Literal["Price", "Delta", "Premium"] = "Price",
        exercise_type: Literal["European", "American"] = "European",
    ):
        if isinstance(start_date, str):
            start_date = date_from_iso_format(start_date)
        if isinstance(maturity_date, str):
            maturity_date = date_from_iso_format(maturity_date)

        if not isinstance(over, str):
            raise ValueError("over must be str")
        if not isinstance(under, str):
            raise ValueError("under must be str")
        if not (
            isinstance(strike, (float, int))
            or (
                isinstance(strike, str)
                and re.match(r"^(SPOT|FWD)([+-]\d{1,2}%)?$", strike)
            )
        ):
            raise ValueError(
                "strike must be a number or string like: "
                "'SPOT', 'FWD', 'SPOT+10%', 'FWD-5%'"
            )
        if option_type not in ("Call", "Put"):
            raise ValueError("option_type must be 'Call' or 'Put'")
        if exercise_type not in ("European", "American"):
            raise ValueError("exercise_type must be 'European' or 'American'")
        self._over = over
        self._under = under
        self._strike = strike
        self._start_date = start_date
        self._maturity_date = maturity_date
        self._option_type = option_type
        self._exercise_type = exercise_type
        if isinstance(strike, str) and "FWD" in strike:
            strike = strike.replace("FWD", "FORWARD")
        api_response = env().client.instruments.otc.fx_option.create(
            session_id=env().session_id,
            strike=strike,
            strike_type=strike_type.upper(),
            type=option_type.upper(),
            exercise_style=exercise_type.upper(),
            start_date=start_date.isoformat(),
            maturity=maturity_date.isoformat(),
            identifier=f"{under}{over} CURNCY",
        )
        self._metrics: Optional[pd.DataFrame] = None
        super().__init__(api_response)

    @property
    def over(self) -> str:
        return self._over

    @property
    def under(self) -> str:
        return self._under

    @property
    def strike(self) -> float:
        return self._get_reference_data()["strike"]

    @property
    def start_date(self) -> dtm.date:
        return self._start_date

    @property
    def maturity_date(self) -> dtm.date:
        return self._maturity_date

    @property
    def option_type(self) -> str:
        return self._option_type

    @property
    def exercise_type(self) -> str:
        return self._exercise_type

    def metrics(self) -> pd.DataFrame:
        if self._metrics is not None:
            return self._metrics

        self.creation_response.wait_for_object_status()
        api_response = env().client.data.history.get(
            session_id=env().session_id,
            object_id=self.api_object_id,
        )

        metrics_df = pd.DataFrame(api_response.history).rename(
            columns={
                "$timestamp": "trading_datetime",
                "$history": "NPV",
                "delta": "Delta",
                "gamma": "Gamma",
                "theta": "Theta",
                "vega": "Vega",
                "impliedVolatility": "ImpliedVolatility",
                "premiumAdjustedDelta": "PA Delta",
            }
        )
        metrics_df = metrics_df.set_index("trading_datetime")
        metrics_df.index = pd.to_datetime(metrics_df.index)
        self._metrics = metrics_df
        assert isinstance(self._metrics, pd.DataFrame)
        return self._metrics

    def data_df(self) -> pd.DataFrame:
        return self.metrics()[["NPV", "ImpliedVolatility"]]

    def history(self) -> pd.Series:
        return self.metrics()["NPV"]
