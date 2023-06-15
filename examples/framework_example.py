import sigtech.api as sig
import datetime as dtm

# sig.ClientSettings.SIGTECH_API_URL = ''
sig.ClientSettings.SIGTECH_API_KEY = 'none'

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

top_basket = sig.BasketStrategy(constituent_names=[basket.name, gc_future.name, si_future.name],
                                weights=[0.5, 0.25, 0.25], rebalance_frequency='EOM', currency='USD',
                                start_date=dtm.date(2019, 2, 1))

print(top_basket.history())
