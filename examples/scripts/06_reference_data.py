import logging

import sigtech.api as sig

logging.basicConfig(level=logging.ERROR)
sig.init()

# Rolling futures strategy (rolling_rule=front)
es_future = sig.RollingFutureStrategy(
    currency="USD",
    start_date="2020-01-08",
    contract_code="ES",
    contract_sector="INDEX",
    rolling_rule="front",
    front_offset="-6,-5",
)
assert es_future.currency == "USD"
print(es_future.rolling_rule)
print(es_future.front_offset)
print(es_future.monthly_roll_days)
es_group = es_future.group()
print(es_group.contract_size)
print(es_group.asset_description)
print(es_group.currency)

# Future
esh19_index = sig.obj.get("ESH19 INDEX")
print(esh19_index.currency)  # type: ignore[union-attr]
print(esh19_index.contract_size)  # type: ignore[union-attr]
print(esh19_index.first_delivery_notice_date)  # type: ignore[union-attr]
print(esh19_index.expiry_date)  # type: ignore[union-attr]
print(esh19_index.futvalpt)  # type: ignore[union-attr]
esh19_group = esh19_index.group()  # type: ignore[union-attr]
print(esh19_group.contract_size)  # type: ignore[union-attr]
print(esh19_group.asset_description)  # type: ignore[union-attr]
print(esh19_group.currency)  # type: ignore[union-attr]

# Index
spx_index = sig.obj.get("SPX INDEX")  # type: ignore[union-attr]
print(spx_index.currency)  # type: ignore[union-attr]
print(spx_index.description)  # type: ignore[union-attr]

# FX
usdjpy = sig.obj.get("USDJPY CURNCY")  # type: ignore[union-attr]
print(usdjpy.currency)  # type: ignore[union-attr]

# Reinvestment strategy (Stock)
apple_stock = sig.get_single_stock_strategy(exchange_ticker="AAPL")
print(apple_stock.currency)  # type: ignore[union-attr]

# Reinvestment strategy (ETF)
agg_etf = sig.get_single_stock_strategy(ticker="AGG UP EQUITY")
print(agg_etf.currency)

# Rolling futures strategy (rolling_rule=F_O)
co_future = sig.RollingFutureStrategy(
    contract_code="CO",
    contract_sector="COMDTY",
)
print(co_future.rolling_rule)
print(co_future.monthly_roll_days)

# Cash
chf_cash = sig.obj.get("CHF CASH")
print(chf_cash.currency)  # type: ignore[union-attr]
