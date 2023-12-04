import datetime as dtm
import logging
from typing import Optional

import numpy as np
import pandas as pd

from sigtech.api.framework.environment import env

logger = logging.getLogger(__name__)


class PlotWrapper:
    def __init__(self, strategy):
        super().__init__()
        self._strategy = strategy

    def _portfolio_df(
        self,
        dts: Optional[str] = None,
        tzinfo=None,
        flatten: Optional[bool] = False,
        start_dt: Optional[dtm.datetime] = None,
        end_dt: Optional[dtm.datetime] = None,
        unit_type: Optional[str] = "MODEL",
    ):
        valid_dts = {
            "VALUATION_PTS": "VALUATION",
            "ACTION_PTS": "ACTION",
            "TOP_ORDER_PTS": "TOP_ORDER",
            None: "LATEST",
        }
        try:
            points = valid_dts[dts]
        except KeyError:
            raise ValueError(f"dts must be one of: {list(valid_dts)}")

        if tzinfo is not None:
            raise ValueError("tzinfo must be None")
        if start_dt is not None:
            raise ValueError("start_dt must be None")
        if end_dt is not None:
            raise ValueError("end_dt must be None")
        if unit_type not in ("MODEL", "TRADE"):
            raise ValueError("unit_type must be 'MODEL' or 'TRADE'")

        logger.debug("Waiting for strategy to complete.")
        self._strategy.creation_response.wait_for_object_status()

        logger.debug("Create portfolio analytics object")
        resp = env().client.analytics.portfolio.create(
            session_id=env().session_id,
            strategy=self._strategy.api_object_id,
            points=points,
            flatten=flatten,
        )
        resp.wait_for_object_status()
        logger.debug("Done creating portfolio analytics object")

        page_size = 25_000

        # Fetch all history pages
        logger.debug("Fetching history for portfolio analytics object")
        page = env().client.performance.history.get(
            session_id=env().session_id,
            object_id=resp.object_id,
            page_size=page_size,
        )
        history = page.history
        while "next_page_id" in page.d:
            logger.debug(
                "Fetching next history page for "
                f"portfolio analytics object: {page.next_page_id}."
            )
            page = env().client.performance.history.get(
                session_id=env().session_id,
                object_id=resp.object_id,
                page_size=page_size,
                page_id=page.next_page_id,
            )
            _update_history(history, page.history)
        history["$timestamp"] = pd.DatetimeIndex(history["$timestamp"])
        history["executionTime"] = pd.DatetimeIndex(history["executionTime"])
        history["type"] = pd.Categorical(
            history["type"],
            categories=[
                "STRATEGY",
                "STRATEGY_ORDER",
                "GROUPED_ORDER",
                "CASH",
                "POSITION",
                "ORDER",
                "FX_SPOT_ORDER",
            ],
        )
        df = pd.DataFrame(history)
        df = df.set_index(["$timestamp", "level", "name"])
        return df

    def portfolio_table(
        self,
        dts: Optional[str] = None,
        tzinfo=None,
        flatten: Optional[bool] = False,
        start_dt: Optional[dtm.datetime] = None,
        end_dt: Optional[dtm.datetime] = None,
        unit_type: Optional[str] = "MODEL",
        as_df: bool = False,
    ):
        if as_df is not True:
            raise ValueError("as_df must be True")
        df = self._portfolio_df(
            dts=dts,
            tzinfo=tzinfo,
            flatten=flatten,
            start_dt=start_dt,
            end_dt=end_dt,
            unit_type=unit_type,
        )
        df = df.reset_index()

        # Transform to framework format
        if unit_type == "MODEL":
            units_column = "quantity"
        elif unit_type == "TRADE":
            units_column = "tradeQuantity"
        else:
            raise NotImplementedError
        df = df[
            [
                "$timestamp",
                "name",
                "level",
                "executionTime",
                "weight",
                "exposureWeight",
                "valuation",
                units_column,
                "value",
                "valueLocal",
                "type",
            ]
        ]
        df["type"] = df["type"].replace(
            {
                "STRATEGY": "Strategy",
                "STRATEGY_ORDER": "Strategy Order",
                "GROUPED_ORDER": "Grouped Order",
                "CASH": "Cash",
                "POSITION": "Position",
                "ORDER": "Order",
                "FX_SPOT_ORDER": "FX Spot Order",
            }
        )
        df = df.rename(
            columns={
                "$timestamp": "Date",
                "name": "Name",
                "level": "Level",
                "executionTime": "Execution Time",
                "weight": "Weight",
                "exposureWeight": "Exp. Weight",
                "valuation": "Valuation",
                units_column: "Units",
                "value": "Value (USD)",
                "valueLocal": "Value (local)",
                "type": "Position Type",
            }
        )
        dt_cols = df.select_dtypes(include=["datetime64[ns]"]).columns
        df[dt_cols] = (
            df[dt_cols]
            .apply(lambda o: o.dt.strftime("%Y/%m/%d, %H:%M:%S"), axis="columns")
            .replace(np.nan, "-")
        )
        float_cols = df.select_dtypes(include=["floating"]).columns
        weight_cols = [o for o in float_cols if "weight" in o.lower()]
        df[float_cols] = df[float_cols].round(3).astype(str)
        df[weight_cols] = df[weight_cols] + "%"
        df[float_cols] = df[float_cols].replace(["nan", "nan%"], "-")
        df = df.replace([None, np.nan], "-")
        df = df.set_index(["Date", "Name", "Level"])
        return df


def _update_history(history, d):
    assert history.keys() == d.keys()
    for k, v in history.items():
        assert isinstance(k, str)
        assert isinstance(v, list)
        v.extend(d[k])
