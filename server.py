import asyncio

from aiohttp import web

from data_manager import DataManager
from views import calc as view_calc
from views import main as view_main


async def init(data_manager) -> web.Application:
    app = web.Application()
    app['data_manager'] = data_manager
    app.add_routes(
        [
            web.get('/', view_main),
            web.get('/{currency:[A-Z]{3}}/{summ}', view_calc),
        ]
    )
    return app


def start_server(data_store, rates_sources, update_frequency,
                 host, port) -> None:
    loop = asyncio.get_event_loop()

    data_manager = DataManager(data_store, rates_sources, update_frequency)
    app = loop.run_until_complete(init(data_manager))
    web.run_app(app, host=host, port=port)


if __name__ == "__main__":
    from data_store import SqliteDataStore
    from rates_source import CbrRatesSource, EcbRatesSource
    from settings import (API_HOST, API_PORT, EXCHANGE_RATE_UPDATE_FREQUENCY,
                          SQLITE_PARAMS)

    data_store = SqliteDataStore(SQLITE_PARAMS)
    asyncio.get_event_loop().run_until_complete(data_store.create_schema())

    rates_sources = [EcbRatesSource(), CbrRatesSource(), ]

    update_frequency = EXCHANGE_RATE_UPDATE_FREQUENCY

    start_server(
        data_store, rates_sources, update_frequency, API_HOST, API_PORT
    )
