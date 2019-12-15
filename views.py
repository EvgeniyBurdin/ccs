from aiohttp import web

from data_type import RatesInfo
from settings import AVAILABLE_CURRENCIES
from utils import calc_currency_summ


async def main(request) -> web.json_response:
    """
        Information about current rates.
    """
    rates_info: RatesInfo = await request.app['data_manager'].get_rates_info()
    return web.json_response(rates_info.as_dict())


async def calc(request) -> web.json_response:
    """
        Information about:
        1. Current rates
        2. The request received
        3. Result amounts for all available currencies
    """
    rates_info: RatesInfo = await request.app['data_manager'].get_rates_info()

    query_currency = request.match_info.get('currency')
    if query_currency not in AVAILABLE_CURRENCIES:
        return web.json_response(
            "'%s' currency not available!" % query_currency,
            status=422
        )
    query_summ = float(request.match_info.get('summ'))

    result = {
        currency: calc_currency_summ(
            result_currency_rate=rates_info.rates[currency],
            base_currency_rate=rates_info.rates[query_currency],
            base_currency_summ=query_summ
        )
        for currency in AVAILABLE_CURRENCIES
        if currency != query_currency
    }

    return web.json_response(
        {
            'rates_info': rates_info.as_dict(),
            'query': {query_currency: query_summ},
            'result': result
        }
    )
