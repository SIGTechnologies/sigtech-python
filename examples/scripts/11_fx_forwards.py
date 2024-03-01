import logging

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()


# Create a single EUR/USD FX Forward at fair rate
fx_forward = sig.FXForward(
    over="USD",  # Quote Currency
    under="EUR",  # Base Currency
    start_date="2021-07-05",
    payment_date="2024-07-05",
)
print(fx_forward.history())

# Create a single GBP/USD FX Forward at rate=1.3
fx_forward = sig.FXForward(
    over="USD",  # Quote Currency
    under="GBP",  # Base Currency
    start_date="2021-07-05",
    payment_date="2024-07-05",
    strike=1.3,
)
print(fx_forward.history())

# Print reference data for the forward
print("name", fx_forward.name)
print("over", fx_forward.over)
print("under", fx_forward.under)
print("start_date", fx_forward.start_date)
print("payment_date", fx_forward.payment_date)
print("strike", fx_forward.strike)


# Create a strategy that regularly buys EUR/USD FX forwards
# every 3 months on IMM dates
rolling_fx_forward = sig.RollingFXForwardStrategy(
    currency="USD",
    long_currency="EUR",
    forward_tenor="3M_IMM",
    start_date="2007-01-01",
)
print(rolling_fx_forward.history())

# Reference data for the strategy
print("currency", rolling_fx_forward.currency)
print("long_currency", rolling_fx_forward.long_currency)
print("forward_tenor", rolling_fx_forward.forward_tenor)
print("start_date", rolling_fx_forward.start_date)

# Portfolio holdings table for the strategy
df_valuation_pts = rolling_fx_forward.plot.portfolio_table(
    dts="ACTION_PTS",
    unit_type="TRADE",
    flatten=True,
    as_df=True,
)
print(df_valuation_pts)
