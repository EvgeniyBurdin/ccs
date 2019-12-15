from data_manager import DataManager
from data_store import SqliteDataStore
from rates_source import FakeRatesSource
from server import init


async def test_main(aiohttp_client, aiohttp_server, params_sqlite):
    data_store = SqliteDataStore(params_sqlite)
    rates_sources = [FakeRatesSource(), ]
    data_manager = DataManager(data_store, rates_sources, 60 * 60 * 25)
    app = await init(data_manager)
    server = await aiohttp_server(app)
    client = await aiohttp_client(server)
    resp = await client.get('/')

    assert resp.status == 200
    # ...


async def test_calc(aiohttp_client, aiohttp_server, params_sqlite):
    data_store = SqliteDataStore(params_sqlite)
    rates_sources = [FakeRatesSource(), ]
    data_manager = DataManager(data_store, rates_sources, 60 * 60 * 25)
    app = await init(data_manager)
    server = await aiohttp_server(app)
    client = await aiohttp_client(server)
    resp = await client.get('/USD/2')

    assert resp.status == 200
    # ...
