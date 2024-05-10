import logging

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()


# Create a strategy to buy a bond and reinvest coupons
single_bond = sig.SingleBondStrategy(
    currency="USD",
    bond_name="US 2.25 2046/08/15 GOVT",  # US912810RT79
)
print(single_bond.history())
print(single_bond.currency)
print(single_bond.start_date)


# Create a strategy to regularly buy bonds and reinvest coupons
rolling_bond_strategy = sig.RollingBondStrategy(
    country="US",
    tenor="10Y",
    start_date="2016-08-15",
)
print(rolling_bond_strategy.history())
print(rolling_bond_strategy.currency)
print(rolling_bond_strategy.tenor)
print(rolling_bond_strategy.country)
print(rolling_bond_strategy.start_date)

df_portfolio_timeline = rolling_bond_strategy.plot.portfolio_table(
    dts="ACTION_PTS",
    unit_type="TRADE",
    as_df=True,
)
print(df_portfolio_timeline)
