import datetime as dtm
import logging
import os

import numpy as np
import pandas as pd

import sigtech.api as sig

logging.basicConfig(level=logging.DEBUG)

assert "SIGTECH_API_KEY" in os.environ

env = sig.init()

sig.env()[sig.config.DISABLE_T_COST_NETTING] = False
env[sig.config.EXCESS_RETURN_ONLY] = False
env[sig.config.TM_TIMEZONE] = "Europe/London"

vg_future = sig.RollingFutureStrategy(
    contract_code="VG",
    contract_sector="INDEX",
    rolling_rule="front",
    front_offset="-4,-4",
    total_return=False,
)
print(vg_future.name)

es_future = sig.RollingFutureStrategy(contract_code="ES", contract_sector="INDEX")
gc_future = sig.RollingFutureStrategy(contract_code="GC", contract_sector="COMDTY")
si_future = sig.RollingFutureStrategy(contract_code="SI", contract_sector="COMDTY")

basket = sig.BasketStrategy(
    constituent_names=[vg_future.name, es_future.name],
    weights=[0.5, 0.5],
    rebalance_frequency="EOM",
    currency="USD",
    start_date=dtm.date(2019, 2, 1),
)

print(gc_future.history())

print(si_future.history())

top_basket = sig.BasketStrategy(
    constituent_names=[
        basket.name,
        gc_future.name,
        si_future.name,
        "EUR CASH",
        "GBPUSD CURNCY",
    ],
    weights=[0.5, 0.125, 0.125, 0.125, 0.125],
    rebalance_frequency="EOM",
    currency="USD",
    start_date=dtm.date(2019, 2, 1),
)

print(top_basket.history())

signal_df = pd.DataFrame(
    0.5
    * (
        pd.concat(
            [gc_future.history(), si_future.history()],
            axis=1,
            names=[gc_future.name, si_future.name],
        )
        .dropna()
        .pct_change()
        .rolling(window=252)
        .mean()
        .dropna()
        .apply(np.sign, axis=1)
    )
)

signal_strategy = sig.SignalStrategy(signal_input=signal_df, currency="USD")

print(signal_strategy.history())
