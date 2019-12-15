import asyncio

from data_store import SqliteDataStore
from rates_source import CbrRatesSource, EcbRatesSource
from server import start_server
from settings import (API_HOST, API_PORT, EXCHANGE_RATE_UPDATE_FREQUENCY,
                      SQLITE_PARAMS)

data_store = SqliteDataStore(SQLITE_PARAMS)
asyncio.get_event_loop().run_until_complete(data_store.create_schema())

rates_sources = [EcbRatesSource(), CbrRatesSource(), ]

update_frequency = EXCHANGE_RATE_UPDATE_FREQUENCY

start_server(
    data_store, rates_sources, update_frequency, API_HOST, API_PORT
)
