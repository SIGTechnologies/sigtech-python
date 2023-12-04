import datetime as dtm
import logging
import os

import sigtech.api as sig

logging.basicConfig(level=logging.DEBUG)

assert "SIGTECH_API_KEY" in os.environ

env = sig.init()

sig.env()[sig.config.DISABLE_T_COST_NETTING] = False
env[sig.config.EXCESS_RETURN_ONLY] = False
env[sig.config.TM_TIMEZONE] = "Europe/London"

gold_etf = sig.ReinvestmentStrategy(underlyer="GLD UP EQUITY")

apple_stock = sig.get_single_stock_strategy(exchange_ticker="AAPL")

apple_etf_basket = sig.BasketStrategy(
    constituent_names=[apple_stock.name, gold_etf.name],
    weights=[0.5, 0.5],
    rebalance_frequency="EOM",
    currency="USD",
    start_date=dtm.date(2019, 2, 1),
    ticker="50-50 APPLE AND GOLD",
)

print(apple_etf_basket.history())

stocks = sig.get_single_stock_strategy(
    exchange_tickers=["AAPL", "META", "GOOGL", "NVDA", "MSFT"]
)

stock_basket = sig.BasketStrategy(
    constituent_names=[stock.name for stock in stocks],
    weights=[1.0 / len(stocks)] * len(stocks),
    rebalance_frequency="EOM",
    currency="USD",
    start_date=dtm.date(2023, 1, 2),
    ticker="STOCK BASKET",
)

print(stock_basket.history())
