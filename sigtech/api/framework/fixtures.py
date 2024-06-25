from sigtech.api.framework.instruments.option_groups import (
    EquityIndexOTCOptionsGroup,
    FXOTCOptionsGroup,
)

FIXTURES = {
    "SPX INDEX OTC OPTION GROUP": EquityIndexOTCOptionsGroup(
        name="SPX INDEX OTC OPTION GROUP",
    ),
    "NDX INDEX OTC OPTION GROUP": EquityIndexOTCOptionsGroup(
        name="NDX INDEX OTC OPTION GROUP",
    ),
    "NKY INDEX OTC OPTION GROUP": EquityIndexOTCOptionsGroup(
        name="NKY INDEX OTC OPTION GROUP",
    ),
    "RTY INDEX OTC OPTION GROUP": EquityIndexOTCOptionsGroup(
        name="RTY INDEX OTC OPTION GROUP",
    ),
    "SX5E INDEX OTC OPTION GROUP": EquityIndexOTCOptionsGroup(
        name="SX5E INDEX OTC OPTION GROUP",
    ),
    "VIX INDEX OTC OPTION GROUP": EquityIndexOTCOptionsGroup(
        name="VIX INDEX OTC OPTION GROUP",
    ),
    "EURUSD OTC OPTION GROUP": FXOTCOptionsGroup(
        name="EURUSD OTC OPTION GROUP",
    ),
    "GBPUSD OTC OPTION GROUP": FXOTCOptionsGroup(
        name="GBPUSD OTC OPTION GROUP",
    ),
    "USDCHF OTC OPTION GROUP": FXOTCOptionsGroup(
        name="USDCHF OTC OPTION GROUP",
    ),
    "USDJPY OTC OPTION GROUP": FXOTCOptionsGroup(
        name="USDJPY OTC OPTION GROUP",
    ),
}
