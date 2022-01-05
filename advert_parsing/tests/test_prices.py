from advert_parsing.markdown_parser import Text
from advert_parsing.classification.prices import find_prices_in_text, PriceTag, Currency, price_regexes


def test_find_prices_in_text():

    t = Text(text="something $40 something")
    prices = find_prices_in_text(t)
    assert prices == [PriceTag(currency=Currency.USD, amount=40., striked=False)]
