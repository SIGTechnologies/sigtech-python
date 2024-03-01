import datetime as dtm
import logging

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()

# Create EUR 2-Year Interest-Rate Swap (IRS) at fair rate:
# - trade date on 2021-07-05 (when swap is agreed, start-date is trade_date+2)
swap_fair = sig.InterestRateSwap(
    currency="EUR",
    tenor="2Y",
    trade_date="2021-07-05",
)
# Print the price, fairRate, pv01
print(swap_fair.data_df())

# Print price history
print(swap_fair.history())

# Create USD 1-Year Interest-Rate Swap (IRS) with fixed rate:
# - trade date on 2021-07-05 (when swap is agreed)
# - start date on 2021-10-05 (when payments begin)
swap = sig.InterestRateSwap(
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
print("fixed_day_count", swap.fixed_day_count)
print("float_day_count", swap.float_day_count)
print("fixed_frequency", swap.fixed_frequency)
print("floating_frequency", swap.floating_frequency)
print("index", swap.index)
