from datetime import datetime

from utils import datetime_to_str, calc_currency_summ


def test_datetime_to_str():
    date_time_str = datetime_to_str(datetime(2019, 12, 13, 17, 10, 10))
    assert date_time_str == '2019-12-13 17:10:10'


def test_calc_currency_summ():
    summ = calc_currency_summ(
        result_currency_rate=2,
        base_currency_rate=6,
        base_currency_summ=3)
    assert summ == 1
