from datetime import datetime


def datetime_to_str(date_time: datetime) -> str:
    return date_time.strftime('%Y-%m-%d %H:%M:%S')


def calc_currency_summ(result_currency_rate: float,
                       base_currency_rate: float,
                       base_currency_summ: float) -> float:
    return base_currency_summ / base_currency_rate * result_currency_rate
