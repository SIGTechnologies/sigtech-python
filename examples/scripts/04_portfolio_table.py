import logging
import os

import sigtech.api as sig

logging.basicConfig(level=logging.DEBUG)

os.environ["SIGTECH_API_KEY"] = "<YOUR_API_KEY>"


env = sig.init()
env[sig.config.TM_TIMEZONE] = "Europe/London"

es_future = sig.RollingFutureStrategy(
    contract_code="ES",
    start_date="2022-01-04",
    contract_sector="INDEX",
)

df_latest = es_future.plot.portfolio_table(
    dts=None,
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)

df_valuation_pts = es_future.plot.portfolio_table(
    dts="VALUATION_PTS",
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)

df_actions_pts = es_future.plot.portfolio_table(
    dts="ACTION_PTS",
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)


df_top_order_pts_flattened = es_future.plot.portfolio_table(
    dts="TOP_ORDER_PTS",
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)

print(df_top_order_pts_flattened.tail(20).to_string())
