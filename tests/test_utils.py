import pytest

from rosetta_sip_factory.utils import clean_title


@pytest.mark.parametrize(
    "title, expected",
    [
        pytest.param(
            "COVID-19 (novel coronavirus) update – 25 March 2020",
            "COVID-19 (novel coronavirus) update - 25 March 2020",
        ),
    ],
)
def test_clean_title(title, expected):
    assert clean_title(title) == expected
