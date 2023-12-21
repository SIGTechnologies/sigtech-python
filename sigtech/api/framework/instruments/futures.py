import datetime as dtm
from typing import Optional

from sigtech.api.client.utils import date_from_iso_format
from sigtech.api.framework.instruments.base import Instrument


class Future(Instrument):
    @property
    def contract_size(self) -> float:
        return self._get_reference_data()["contractSize"]

    @property
    def expiry_date(self) -> Optional[dtm.date]:
        x = self._get_reference_data()["expiryDate"]
        return date_from_iso_format(x) if x else None

    @property
    def first_delivery_notice_date(self) -> Optional[dtm.date]:
        x = self._get_reference_data()["firstDeliveryNoticeDate"]
        return date_from_iso_format(x) if x else None

    @property
    def futvalpt(self) -> Optional[float]:
        x = self._get_reference_data()["pointValue"]
        return float(x) if x else None

    def group(self):
        d = self._get_reference_data()["$group"]
        return FuturesContractGroup(d)


class FuturesContractGroup:
    def __init__(self, d: dict):
        self._d = d
        super().__init__()

    @property
    def currency(self):
        return self._d["currency"]

    @property
    def asset_description(self):
        return self._d["description"]

    @property
    def contract_size(self):
        return self._d["contractSize"]
