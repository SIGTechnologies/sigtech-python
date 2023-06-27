import os
import sigtech.api as sig
import datetime as dtm
import pandas as pd
import numpy as np

os.environ['SIGTECH_API_KEY'] = '' #ENTER API KEY#

sig.init()

vg_future = sig.RollingFutureStrategy(contract_code='VG', contract_sector='INDEX', rolling_rule='front',
                                      front_offset='-4:-1')
es_future = sig.RollingFutureStrategy(contract_code='ES', contract_sector='INDEX')
gc_future = sig.RollingFutureStrategy(contract_code='GC', contract_sector='COMDTY', start_date=dtm.date(2017, 2, 8))
si_future = sig.RollingFutureStrategy(contract_code='SI', contract_sector='COMDTY', start_date=dtm.date(2017, 2, 8))

basket = sig.BasketStrategy(constituent_names=[vg_future.name, es_future.name], weights=[0.5, 0.5],
                            rebalance_frequency='EOM', currency='USD', start_date=dtm.date(2019, 2, 1))

print(gc_future.history())

print(si_future.history())

top_basket = sig.BasketStrategy(constituent_names=[basket.name, gc_future.name, si_future.name, 'EUR CASH'],
                                weights=[0.5, 0.25, 0.125, 0.125], rebalance_frequency='EOM', currency='USD',
                                start_date=dtm.date(2019, 2, 1))

print(top_basket.history())

signal_df = 0.5 * np.sign(pd.concat([gc_future.history(), si_future.history()], axis=1).dropna().pct_change().rolling(window=252).mean().dropna())
signal_df.columns = [gc_future.name, si_future.name]

signal_strategy = sig.SignalStrategy(signal_input=signal_df, currency='USD')

print(signal_strategy.history())