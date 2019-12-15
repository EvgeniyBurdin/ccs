from dataclasses import FrozenInstanceError

import pytest


def test_rates_info_as_dict(rates_info, dict_rates_info):
    assert dict_rates_info == rates_info.as_dict()


def test_frozen_rates_info(rates_info):
    with pytest.raises(FrozenInstanceError):
        rates_info.source = 'new_source'
