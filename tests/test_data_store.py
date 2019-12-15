import aiosqlite
import pytest

from data_type import RatesInfo


class TestSqliteDataStore():

    @pytest.mark.asyncio
    async def test_get_connection(self, sqlite_db):
        connection = await sqlite_db.get_connection()
        assert isinstance(connection, aiosqlite.Connection)

    @pytest.mark.asyncio
    async def test_read_newest_row(self, sqlite_db, dict_rates_info):
        dict_rates_info['date_parse'] = '2019-12-14 15:13:25+00'
        rates_info = RatesInfo(**dict_rates_info)
        await sqlite_db.save_row(rates_info)

        dict_rates_info['date_parse'] = '2019-01-01 15:13:25+00'
        await sqlite_db.save_row(RatesInfo(**dict_rates_info))

        readed_rates_info = await sqlite_db.read_newest_row()
        assert rates_info == readed_rates_info
