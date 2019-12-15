import pytest

from data_store import SqliteDataStore
from data_type import RatesInfo


@pytest.fixture
def dict_rates_info():
    return {
        'source':'https://www.ecb.europa.eu/stats/eurofxref/eurofxref-daily.xml',  # noqa
        'date_source': '2019-12-13',
        'base_currency': 'EUR',
        'date_parse': '2019-12-14 15:13:25+00',
        'rates': {'CZK': 25.508, 'EUR': 1, 'PLN': 4.2726, 'USD': 1.1174}
    }


@pytest.fixture
def rates_info(dict_rates_info):
    return RatesInfo(**dict_rates_info)


@pytest.fixture(scope='session')
def params_sqlite(tmpdir_factory):
    temp_dir = tmpdir_factory.mktemp('temp')
    filename = temp_dir.join('test_rates.db')
    yield {'NAME': filename}


@pytest.fixture
async def sqlite_db(params_sqlite):
    db = SqliteDataStore(params_sqlite)
    await db.create_schema()
    await db.delete_all()
    yield db
