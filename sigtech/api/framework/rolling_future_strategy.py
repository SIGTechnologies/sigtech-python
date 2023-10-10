import datetime as dtm
from typing import Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategy_base import StrategyBase


class RollingFutureStrategy(StrategyBase):
    """
    RollingFutureStrategy class implements rolling future strategies,
    potentially rolled over multiple days.

    :param contract_code: Contract code for futures contract group to trade.
    :param contract_sector: Contract sector for futures contract group to trade.
    :param currency: Base strategy currency for initial cash and valuation,
                    (optional) defaults to future currency.
    :param rolling_rule: Rule to apply when rolling. Common options include
                        'front' and 'f_0'.
    :param front_offset: If using 'front' as 'rolling_rule', this parameter
                        specifies the number of business days before the
                        first delivery notice date (or expiry date for cash
                        settled futures) to start and finish the roll. The
                        date range is indexed in Python notation, e.g.
                        '-5:-3' will roll half the contracts 5 days before
                        expiry and roll the other half 4 days before
                        contract expiry (indexed one away from -3). If
                        'rolling_rule' is not 'front', this argument is
                        ignored.
    :param start_date: Start of strategy (optional).
    :param monthly_roll_days: Defines which business day of the month to
                            roll the contracts on. Only required if
                            'rolling_rule' is not set to 'front' or
                            'prev_month'. If None, will default to '5:9'
                            unless 'rici' rule is used.
    :param total_return: Determines if interest is accrued on cash held within
                         the strategy.
    """

    def __init__(
        self,
        contract_code: str,
        contract_sector: str,
        currency: Optional[str] = None,
        rolling_rule: Optional[str] = None,
        front_offset: Optional[str] = None,
        start_date: Optional[Union[str, dtm.date]] = None,
        monthly_roll_days: Optional[str] = None,
        total_return: Optional[bool] = None,
    ):
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        super().__init__(
            contract_code=contract_code,
            contract_sector=contract_sector,
            currency=currency,
            rolling_rule=rolling_rule,
            front_offset=front_offset,
            start_date=start_date,
            monthly_roll_days=monthly_roll_days,
            total_return=total_return,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch rolling future strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        api_inputs["identifier"] = (
            api_inputs["contract_code"] + " " + api_inputs["contract_sector"]
        )
        del api_inputs["contract_code"]
        del api_inputs["contract_sector"]

        return env().client.strategies.futures.rolling.create(
            session_id=session_id,
            **api_inputs,
        )
