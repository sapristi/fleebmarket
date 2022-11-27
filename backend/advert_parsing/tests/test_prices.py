from advert_parsing.classification.prices import (
    Currency,
    PriceTag,
    find_prices_in_text,
    price_regexes,
)
from advert_parsing.markdown_parser import Text


def test_find_prices_in_text():

    t = Text(text="something $40 something")
    prices = find_prices_in_text(t)
    assert prices == [PriceTag(currency=Currency.USD, amount=40.0, striked=False)]


def test_find_prices_bought_for():
    text = Text(
        text="""
Originally bought for $100, selling for $60 shipped, bought for $100
    """
    )
    prices = find_prices_in_text(text)
    assert len(prices) == 1
    assert prices[0].amount == 60
