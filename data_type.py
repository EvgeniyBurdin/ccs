from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class RatesInfo:
    source: str
    date_source: str
    base_currency: str
    date_parse: str
    rates: Dict[str, float]

    def as_dict(self):
        return {
            'source': self.source,
            'date_source': self.date_source,
            'base_currency': self.base_currency,
            'date_parse': self.date_parse,
            'rates': self.rates
        }
