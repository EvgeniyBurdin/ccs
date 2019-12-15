import json
from abc import ABC, abstractmethod
from typing import Optional

import aiosqlite

from data_type import RatesInfo


class AbstractDataStore(ABC):
    def __init__(self, params: dict) -> None:
        self.params = params

    @abstractmethod
    def get_connection(self) -> object:
        pass

    @abstractmethod
    def read_newest_row(self, date) -> RatesInfo:
        pass

    @abstractmethod
    def save_row(self, rates_info: RatesInfo) -> None:
        pass


class SqliteDataStore(AbstractDataStore):

    async def get_connection(self) -> object:
        return await aiosqlite.connect(self.params['NAME'])

    async def create_schema(self) -> None:
        try:
            connection = await self.get_connection()
            query = '''
                CREATE TABLE rates_info
                (source text, date_source text, base_currency text,
                date_parse text, rates text)
            '''
            await connection.execute(query)
            print('А database of currency exchange rates has been created.')
        except Exception:
            pass  # TODO: add error handling
        finally:
            await connection.close()

    async def read_newest_row(self) -> Optional[RatesInfo]:
        try:
            connection = await self.get_connection()

            query = 'SELECT * FROM rates_info ORDER BY date_parse DESC LIMIT 1'
            cursor = await connection.execute(query)

            row = await cursor.fetchone()
            if row:
                return RatesInfo(
                    source=row[0], date_source=row[1], base_currency=row[2],
                    date_parse=row[3], rates=json.loads(row[4])
                )
            pass  # TODO: add error handling
        finally:
            await connection.close()

    async def save_row(self, rates_info: RatesInfo) -> None:
        try:
            connection = await self.get_connection()
            query = '''
                INSERT INTO rates_info
                (source, date_source, base_currency, date_parse, rates)
                VALUES(?, ?, ?, ?, ?)
            '''
            await connection.execute(
                query, (
                    rates_info.source, rates_info.date_source,
                    rates_info.base_currency, rates_info.date_parse,
                    json.dumps(rates_info.rates)
                )
            )
            await connection.commit()
            pass  # TODO: add error handling
        finally:
            await connection.close()

    async def delete_all(self) -> None:
        try:
            connection = await self.get_connection()
            await connection.execute('DELETE FROM rates_info')
            await connection.commit()
            pass  # TODO: add error handling
        finally:
            await connection.close()
