import datetime as dtm
import logging
import os

import sigtech.api as sig

logging.basicConfig(level=logging.DEBUG)

os.environ.setdefault("SIGTECH_API_KEY", "<YOUR_API_KEY>")

env = sig.init()

sig.env()[sig.config.DISABLE_T_COST_NETTING] = False
env[sig.config.EXCESS_RETURN_ONLY] = False
env[sig.config.TM_TIMEZONE] = "Europe/London"

vg_future = sig.RollingFutureStrategy(
    contract_code="VG",
    contract_sector="INDEX",
    rolling_rule="front",
    front_offset="-4:-3",
    total_return=False,
)
print(vg_future.history())

z_future = sig.RollingFutureStrategy(
    currency="GBP",
    contract_code="Z ",
    contract_sector="INDEX",
    start_date=dtm.date(2023, 1, 1),
    rolling_rule="front",
    front_offset="-6:-4",
    total_return=False,
)
print(z_future.history())
z_future2 = sig.RollingFutureStrategy(
    currency="GBP",
    contract_code="Z",
    contract_sector="INDEX",
    start_date=dtm.date(2023, 1, 1),
    rolling_rule="front",
    front_offset="-6:-4",
    total_return=False,
)
print(z_future2.history())
