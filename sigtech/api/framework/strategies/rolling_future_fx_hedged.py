import datetime as dtm
from typing import Optional, Union

from sigtech.api.client.response import Response
from sigtech.api.framework.environment import env
from sigtech.api.framework.strategies.rolling_future_strategy import (
    RollingFutureStrategy,
)


class RollingFutureFXHedgedStrategy(RollingFutureStrategy):
    """
    An FX-aware version of ``RollingFutureStrategy``, maintaining proper foreign cash
    end exposure positions through maintaining thresholds and rebalancing accordingly.

    In addition to the settings used for class ``RollingFutureStrategy``,
    ``exposure_rebalance_threshold`` and ``cash_rebalance_threshold`` are used to
    control the FX hedging agenda.

    :param cash_rebalance_threshold: once the FX cash exposure breaches the threshold,
                                    the strategy will convert the FX cash to the base
                                    currency.
    :param exposure_rebalance_threshold: once the underlying future's FX exposure
                                    breaches the threshold, the strategy will buy/sell
                                    certain amount of underlying future to control the
                                    exposure.
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
        cash_rebalance_threshold: Optional[float] = 0.02,
        exposure_rebalance_threshold: Optional[float] = 0.02,
    ):
        start_date = str(start_date) if isinstance(start_date, dtm.date) else start_date
        contract_code = contract_code.strip()
        super(RollingFutureStrategy, self).__init__(
            contract_code=contract_code,
            contract_sector=contract_sector,
            currency=currency,
            rolling_rule=rolling_rule,
            front_offset=front_offset,
            start_date=start_date,
            monthly_roll_days=monthly_roll_days,
            total_return=total_return,
            cash_rebalance_threshold=cash_rebalance_threshold,
            exposure_rebalance_threshold=exposure_rebalance_threshold,
        )

    def _get_strategy_obj(self, session_id: str, **inputs) -> Response:
        """
        Fetch rolling future fx hedged strategy from API.
        """
        api_inputs = {k: v for k, v in inputs.items() if v is not None}
        api_inputs["identifier"] = (
            api_inputs["contract_code"] + " " + api_inputs["contract_sector"]
        )
        del api_inputs["contract_code"]
        del api_inputs["contract_sector"]

        return env().client.strategies.futures.rolling.fx_hedged.create(
            session_id=session_id,
            **api_inputs,
        )
