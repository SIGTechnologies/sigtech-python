import logging

import numpy as np
import pandas as pd

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()
env[sig.config.EXCESS_RETURN_ONLY] = True

# Create a tradable timeseries
index = pd.bdate_range("2020-01-01", "2024-01-18")
data = np.geomspace(1000, 10000, len(index))
series = pd.Series(index=index, data=data)
tradable_timeseries = sig.TradableTSIndex(
    currency="USD",
    timeseries=series,
    start_date=series.index[0],
)
print(tradable_timeseries.name)
print(tradable_timeseries.history())

# Add to a basket strategy
basket = sig.BasketStrategy(
    currency="USD",
    constituent_names=[tradable_timeseries.name],
    weights=[1.0],
    rebalance_frequency="EOM",
)
print(basket.history())
