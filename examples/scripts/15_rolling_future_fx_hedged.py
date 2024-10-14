import datetime as dtm
import logging
import os

import sigtech.api as sig

logging.basicConfig(level=logging.DEBUG)

assert "SIGTECH_API_KEY" in os.environ

env = sig.init()

vg_future_hedged = sig.RollingFutureFXHedgedStrategy(
    currency="USD",
    start_date=dtm.date(2018, 1, 4),
    contract_code="VG",
    contract_sector="INDEX",
    rolling_rule="front",
    front_offset="-3,-2",
    cash_rebalance_threshold=0.02,
    exposure_rebalance_threshold=0.02,
)

print(vg_future_hedged.history())

# Print reference data
print("name", vg_future_hedged.name)
print("currency", vg_future_hedged.currency)
print("rolling_rule", vg_future_hedged.rolling_rule)
print("front_offset", vg_future_hedged.front_offset)

vg_group = vg_future_hedged.group()
print(vg_group.contract_size)
print(vg_group.asset_description)
print(vg_group.currency)

# Portfolio holdings table for the strategy
df_valuation_pts = vg_future_hedged.plot.portfolio_table(
    dts="ACTION_PTS",
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)
print(df_valuation_pts)
