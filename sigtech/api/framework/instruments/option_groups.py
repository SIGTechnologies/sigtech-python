import datetime as dtm
from typing import Literal, Union

from sigtech.api.client.utils import removesuffix
from sigtech.api.framework.instruments.options import EquityIndexOTCOption, FXOTCOption


class FXOTCOptionsGroup:
    def __init__(self, name: str):
        assert name.endswith(" OTC OPTION GROUP")
        self.name = name

    def __repr__(self):
        return f"{self.name} <FXOTCOptionsGroup>[{id(self)}]"

    def get_option(
        self,
        strike: Union[float, str],
        start_date: Union[dtm.date, str],
        maturity: Union[dtm.date, str],
        option_type: Literal["Put", "Call"],
        strike_type: Literal["Price", "Delta", "Premium"] = "Price",
        exercise_type: Literal["European", "American"] = "European",
    ):
        if strike_type in ("SPOT", "FWD"):
            raise ValueError(
                f"strike_type {strike_type} is not currently support by SDK"
            )
        fx_pair = removesuffix(self.name, " OTC OPTION GROUP")
        under, over = fx_pair[0:3], fx_pair[3:6]
        return FXOTCOption(
            under=under,
            over=over,
            strike=strike,
            start_date=start_date,
            maturity_date=maturity,
            option_type=option_type,
            strike_type=strike_type,
            exercise_type=exercise_type,
        )


class EquityIndexOTCOptionsGroup:
    def __init__(self, name):
        assert name.endswith(" OTC OPTION GROUP")
        self.name = name

    def __repr__(self):
        return f"{self.name} <EquityIndexOTCOptionsGroup>[{id(self)}]"

    def get_option(
        self,
        strike: Union[float, str],
        start_date: Union[dtm.date, str],
        maturity: Union[dtm.date, str],
        option_type: Literal["Put", "Call"],
        strike_type: Literal["Price", "Delta", "Premium"] = "Price",
        exercise_type: Literal["European", "American"] = "European",
    ):
        if strike_type in ("SPOT", "FWD"):
            raise ValueError(
                f"strike_type {strike_type} is not currently support by SDK"
            )
        index = removesuffix(self.name, " OTC OPTION GROUP")
        return EquityIndexOTCOption(
            underlying=index,
            strike=strike,
            start_date=start_date,
            maturity_date=maturity,
            option_type=option_type,
            strike_type=strike_type,
            exercise_type=exercise_type,
        )
