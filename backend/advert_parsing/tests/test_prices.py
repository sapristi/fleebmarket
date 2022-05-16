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
