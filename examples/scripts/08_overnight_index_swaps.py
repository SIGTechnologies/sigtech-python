import datetime as dtm
import logging

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()

# Create EUR 2-Year Overnight-Index Swap (OIS) at fair rate:
# - trade date on 2021-07-05 (when swap is agreed, start-date is trade_date+2)
# - paying SOFR and receiving OIS rate
swap_fair = sig.OISSwap(
    currency="EUR",
    tenor="2Y",
    trade_date="2021-07-05",
)
# Print the price, fairRate, pv01
print(swap_fair.data_df())

# Print price history
print(swap_fair.history())

# Create USD 1-Year Overnight-Index Swap (OIS) with fixed rate:
# - trade date on 2021-07-05 (when swap is agreed)
# - start date on 2021-10-05 (when interest payments begin)
# - paying SOFR and receiving 1.32%
swap = sig.OISSwap(
    currency="USD",
    tenor="1Y",
    trade_date="2021-07-05",
    start_date=dtm.date(2021, 10, 5),
    fixed_rate=0.0132,
)

# Print the price, fairRate, pv01
print(swap.data_df())

# Print reference data for the swap
print("name", swap.name)
print("currency", swap.currency)
print("tenor", swap.tenor)
print("trade_date", swap.trade_date)
print("start_date", swap.start_date)
print("maturity", swap.maturity)
print("fixed_rate", swap.fixed_rate)
print("fixing_lag", swap.fixing_lag)
print("pay_delay", swap.pay_delay)
print("settlement_days", swap.settlement_days)
print("day_count", swap.day_count)
print("frequency", swap.frequency)
print("index", swap.index)
