import datetime as dtm
import logging

import sigtech.api as sig

logging.basicConfig(level=logging.INFO)
env = sig.init()


# SPX European Call option at spot price
spx_group = sig.obj.get("SPX INDEX OTC OPTION GROUP")
assert isinstance(spx_group, sig.EquityIndexOTCOptionsGroup)
spx_option = spx_group.get_option(
    start_date=dtm.date(2024, 4, 3),
    maturity=dtm.date(2024, 5, 3),
    strike="SPOT",
    option_type="Call",
)
print(spx_option.strike)
print(spx_option.history())


# SPX American Put option at forward price +10%
spx_group = sig.obj.get("SPX INDEX OTC OPTION GROUP")
assert isinstance(spx_group, sig.EquityIndexOTCOptionsGroup)
spx_option = spx_group.get_option(
    start_date=dtm.date(2024, 4, 3),
    maturity=dtm.date(2024, 5, 3),
    strike="FWD+10%",
    option_type="Put",
    exercise_type="American",
)
print(spx_option.strike)
print(spx_option.history())


# EURUSD Call Option at 0.5 Delta
eurusd_group = sig.obj.get("EURUSD OTC OPTION GROUP")
assert isinstance(eurusd_group, sig.FXOTCOptionsGroup)
eurusd_option = eurusd_group.get_option(
    start_date=dtm.date(2024, 4, 3),
    maturity=dtm.date(2024, 5, 3),
    strike=0.5,
    strike_type="Delta",
    option_type="Call",
)
print(eurusd_option.strike)
print(eurusd_option.history())


# USDJPY Put Option at -0.5 Delta
eurusd_group = sig.obj.get("USDJPY OTC OPTION GROUP")
assert isinstance(eurusd_group, sig.FXOTCOptionsGroup)
eurusd_option = eurusd_group.get_option(
    start_date=dtm.date(2024, 4, 3),
    maturity=dtm.date(2024, 5, 3),
    strike=-0.5,
    strike_type="Delta",
    option_type="Put",
)
print(eurusd_option.strike)
print(eurusd_option.history())


# SPX INDEX Call Option at 5447 strike
spx_option = sig.EquityIndexOTCOption(
    currency="USD",
    underlying="SPX INDEX",
    strike=5447,
    start_date=dtm.date(2024, 5, 24),
    maturity_date=dtm.date(2024, 6, 24),
    option_type="Call",
)
print(spx_option.history())
print(spx_option.metrics())


# EURUSD FX Call Option at 1.07 strike
eurusd_option = sig.FXOTCOption(
    under="EUR",
    over="USD",
    strike=1.07,
    start_date=dtm.date(2024, 6, 3),
    maturity_date=dtm.date(2024, 7, 1),
    option_type="Call",
)
print(eurusd_option.history())
print(eurusd_option.metrics())


# EURUSD straddle at spot price
eurusd_straddle = sig.StraddleOptionStrategy(
    group_name=sig.obj.get("EURUSD OTC OPTION GROUP").name,
    start_date=dtm.date.fromisoformat("2020-01-03"),
    maturity=dtm.date.fromisoformat("2023-02-15"),
    strike_type="SPOT",
)
print(eurusd_straddle.history())


# SPX straddle at 0.5 delta
spx_straddle = sig.StraddleOptionStrategy(
    group_name="SPX INDEX OTC OPTION GROUP",
    start_date="2024-01-03",
    maturity="2024-02-03",
    strike_type="Delta",
    strike=0.5,
)
print(spx_straddle.history())


# SPX straddle at premium 100
spx_straddle = sig.StraddleOptionStrategy(
    group_name=sig.obj.get("SPX INDEX OTC OPTION GROUP").name,
    start_date="2024-01-01",
    maturity="2024-04-01",
    strike_type="Premium",
    strike=100,
)
print(spx_straddle.history())
print(spx_straddle.plot.portfolio_table(as_df=True, dts="ACTION_PTS"))


# SPX straddle rolling monthly at delta 0.5
spx_rolling_straddle = sig.RollingStraddleOptionStrategy(
    currency="USD",
    start_date="2024-01-04",
    group_name=sig.obj.get("SPX INDEX OTC OPTION GROUP").name,
    maturity="1M",
    rolling_frequencies=["1M"],
    strike_type="Delta",
    strike=0.5,
)
print(spx_rolling_straddle.history())
print(spx_rolling_straddle.plot.portfolio_table(as_df=True, dts="ACTION_PTS"))


# EURUSD straddle rolling monthly at spot price
eurusd_rolling_straddle = sig.RollingStraddleOptionStrategy(
    start_date="2024-01-04",
    group_name=sig.obj.get("EURUSD OTC OPTION GROUP").name,
    maturity="1M",
    rolling_frequencies=["1M"],
    strike_type="SPOT",
)
print(eurusd_rolling_straddle.history())
print(eurusd_rolling_straddle.plot.portfolio_table(as_df=True, dts="ACTION_PTS"))
