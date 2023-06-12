import sigtech_api as sig
import datetime as dtm

sig.init()

vg_future = sig.RollingFutureStrategy(contract_code='VG', contract_sector='INDEX', rolling_rule='front',
                                      front_offset='-6:-1')
es_future = sig.RollingFutureStrategy(contract_code='ES', contract_sector='INDEX', rolling_rule='front',
                                      front_offset='-4:-1')
gc_future = sig.RollingFutureStrategy(contract_code='GC', contract_sector='COMDTY', rolling_rule='f_0',
                                      front_offset='-3:-1', monthly_roll_days='1:4')
si_future = sig.RollingFutureStrategy(contract_code='SI', contract_sector='COMDTY', rolling_rule='f_0',
                                      front_offset='-3:-1', monthly_roll_days='1:4')

basket = sig.BasketStrategy(constituent_names=[vg_future.name, es_future.name], weights=[0.5, 0.5],
                            rebalance_frequency='EOM', currency='USD', start_date=dtm.date(2020, 2, 1))

top_basket = sig.BasketStrategy(constituent_names=[basket.name, gc_future.name, si_future.name],
                                weights=[0.5, 0.25, 0.25], rebalance_frequency='EOM', currency='USD',
                                start_date=dtm.date(2020, 2, 1))

print(top_basket.history())
