from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional, Tuple
from xml.dom import minidom

import aiohttp

from data_type import RatesInfo
from settings import AVAILABLE_CURRENCIES
from utils import datetime_to_str


class AbstractRatesSource(ABC):

    available_currencies = AVAILABLE_CURRENCIES

    url: str = None

    # The symbolic code of the base currency in the source list. The rate
    # for this currency is always 1.
    base_currency: str = None

    def __init__(self, available_currencies: Optional[tuple] = None) -> None:

        if available_currencies is not None:
            self.available_currencies = available_currencies

        if self.url is None or self.base_currency is None:
            raise Exception('Error: Source parameters are not set!')

    def _get_only_available_rates(self,
                                  rates: Dict[str, float]) -> Dict[str, float]:
        result = {}
        for currency in self.available_currencies:

            if rates.get(currency) is None:
                if currency == self.base_currency:
                    rates[currency] = 1
                else:
                    error_str = 'Error: "%s" currency not found ' % currency
                    error_str += 'on page "%s"' % self.url
                    raise Exception(error_str)

            if rates[currency] > 0:
                result[currency] = rates[currency]
            else:
                error_str = 'Error: Invalid currency rate '
                error_str += '%s=%s!' % (currency, rates[currency])
                raise Exception(error_str)

        return result

    async def get_info(self) -> RatesInfo:
        text = await self._request()
        date_source, all_rates = self._parse(text)
        rates = self._get_only_available_rates(all_rates)
        date_parse = datetime_to_str(datetime.utcnow()) + '+00'
        return RatesInfo(
            self.url, date_source, self.base_currency, date_parse, rates
        )

    async def _request(self) -> str:
        async with aiohttp.ClientSession() as session:
            async with session.get(self.url) as response:
                return await response.text()

    @abstractmethod
    def _parse(self, text: str) -> Tuple[str, Dict[str, float]]:
        pass


class CbrRatesSource(AbstractRatesSource):

    url = 'http://www.cbr.ru/scripts/XML_daily.asp'
    base_currency = 'RUB'

    def _parse(self, text: str) -> Tuple[str, Dict[str, float]]:

        doc = minidom.parseString(text)
        doc.normalize()

        val_curs = doc.getElementsByTagName('ValCurs')[0]

        date_source = val_curs.getAttribute("Date")

        rates = {}
        info_list = val_curs.childNodes
        for info in info_list:
            fields = info.childNodes
            currency = fields[1].firstChild.data
            nominal = float(fields[2].firstChild.data.replace(',', '.'))
            rate = float(fields[4].firstChild.data.replace(',', '.'))
            rate = rate / nominal
            rates[currency] = 1 / rate  # Since rate in rubles!

        return date_source, rates


class EcbRatesSource(AbstractRatesSource):

    url = 'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml'
    base_currency = 'EUR'

    def _parse(self, text: str) -> Tuple[str, Dict[str, float]]:

        doc = minidom.parseString(text)
        doc.normalize()

        cube = doc.getElementsByTagName('Cube')[0]
        cube = cube.getElementsByTagName('Cube')[0]

        date_source = cube.getAttribute("time")

        info_list = cube.getElementsByTagName('Cube')
        rates = {}
        for info in info_list:
            currency = info.getAttribute("currency")
            rate = info.getAttribute("rate")
            rates[currency] = float(rate)

        return date_source, rates


class FakeRatesSource(EcbRatesSource):
    async def _request(self) -> str:
        return '''<Cube>
                <Cube time="2019-12-13">
                <Cube currency="USD" rate="1.1174"/>
                <Cube currency="JPY" rate="122.43"/>
                <Cube currency="BGN" rate="1.9558"/>
                <Cube currency="CZK" rate="25.508"/>
                <Cube currency="DKK" rate="7.4731"/>
                <Cube currency="GBP" rate="0.83508"/>
                <Cube currency="HUF" rate="328.85"/>
                <Cube currency="PLN" rate="4.2726"/>
                <Cube currency="RON" rate="4.7795"/>
                <Cube currency="SEK" rate="10.4490"/>
                <Cube currency="CHF" rate="1.0982"/>
                <Cube currency="ISK" rate="137.00"/>
                <Cube currency="NOK" rate="10.0630"/>
                <Cube currency="HRK" rate="7.4398"/>
                <Cube currency="RUB" rate="69.9930"/>
                <Cube currency="TRY" rate="6.4822"/>
                <Cube currency="AUD" rate="1.6159"/>
                <Cube currency="BRL" rate="4.5664"/>
                <Cube currency="CAD" rate="1.4712"/>
                <Cube currency="CNY" rate="7.7900"/>
                <Cube currency="HKD" rate="8.7062"/>
                <Cube currency="IDR" rate="15626.84"/>
                <Cube currency="ILS" rate="3.8894"/>
                <Cube currency="INR" rate="79.0610"/>
                <Cube currency="KRW" rate="1308.97"/>
                <Cube currency="MXN" rate="21.2518"/>
                <Cube currency="MYR" rate="4.6199"/>
                <Cube currency="NZD" rate="1.6873"/>
                <Cube currency="PHP" rate="56.441"/>
                <Cube currency="SGD" rate="1.5106"/>
                <Cube currency="THB" rate="33.729"/>
                <Cube currency="ZAR" rate="16.1393"/>
                </Cube>
                </Cube>
         '''
