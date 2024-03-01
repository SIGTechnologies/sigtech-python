import logging

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()

# Create a strategy that regularly buys USD forward-starting IMM swaps
rolling_swap_strategy = sig.RollingSwapStrategy(
    tenor="6M",
    currency="USD",
    rolling_frequency_months=6,
    forward_start_months=9,
    start_date="2007-01-01",
)
print(rolling_swap_strategy.history())

# Reference data for the strategy
print("currency", rolling_swap_strategy.currency)
print("tenor", rolling_swap_strategy.tenor)
print("start_date", rolling_swap_strategy.start_date)
print("forward_start_months", rolling_swap_strategy.forward_start_months)
print("rolling_frequency_months", rolling_swap_strategy.rolling_frequency_months)
print("roll_offset", rolling_swap_strategy.roll_offset)

# Portfolio holdings table for the strategy
df_valuation_pts = rolling_swap_strategy.plot.portfolio_table(
    dts="ACTION_PTS",
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)
print(df_valuation_pts)
