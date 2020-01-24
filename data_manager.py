import asyncio
from typing import List, Optional, NoReturn

from data_store import AbstractDataStore
from data_type import RatesInfo
from rates_source import AbstractRatesSource


class DataManager:
    def __init__(self,
                 data_store: AbstractDataStore,
                 rates_sources: List[AbstractRatesSource],
                 update_frequency: int) -> None:

        self.data_store = data_store
        self.rates_sources = rates_sources
        self.update_frequency = update_frequency

        self._rates_info: Optional[RatesInfo] = None

    async def updater(self) -> NoReturn:
        """
            Сопрограмма периодического обновления курсов
            Интервал обновления хранится в self.update_frequency
        """
        while True:
            await asyncio.sleep(self.update_frequency)
            await self.update_rates_info()

    async def get_rates_info(self) -> RatesInfo:
        if self._rates_info is None:
            asyncio.create_task(self.updater())
            await self.update_rates_info()
        return self._rates_info

    async def read_rates_info_from_db(self) -> RatesInfo:
        return await self.data_store.read_newest_row()

    async def update_rates_info(self) -> None:

        refreshed = False
        for rates_source in self.rates_sources:
            print('Trying to update from the source: "%s"' % rates_source.url)
            try:
                rates_info = await rates_source.get_info()
                print('Rates have been successfully updated from the source!')
                refreshed = True
                break
            except Exception as error:
                error_str = 'Could not update from the source '
                error_str += '"%s"! ' % rates_source.url
                error_str += 'Error: %s' % error
                print(error_str)

        if refreshed:
            await self.data_store.save_row(rates_info)
            self._rates_info = rates_info
            print('DB and rates_info refreshed!', self._rates_info.as_dict())

        if self._rates_info is None:
            self._rates_info = await self.read_rates_info_from_db()
            print('Rates were read from the database!')
