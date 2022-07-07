import re
from enum import Enum
from typing import Optional

from advert_parsing.markdown_parser import LineBreak, Text, ThematicBreak
from pydantic import BaseModel, validator

# capture number, with either . or , as delimiter (non capturing group)
number_group_regex = r"(?P<price>\d+(?:[.,]\d+)?)"


class Currency(str, Enum):
    GBP = "GBP"
    CAD = "CAD"
    AUD = "AUD"
    SGD = "SGD"
    EUR = "EUR"
    USD = "USD"


currencies = {
    Currency.GBP: ["£", "gbp"],
    Currency.CAD: ["CAD"],
    Currency.AUD: ["AUD"],
    Currency.SGD: ["sgd", "sg$", "s$"],
    Currency.EUR: ["eur", "€"],
    Currency.USD: [re.escape("$"), "usd"],
}


def generate_curr_regexes(curr_exprs):
    res = []
    for curr_expr in curr_exprs:
        if curr_expr == r"\\$":
            res.append(
                re.compile(f"{curr_expr} ?{number_group_regex}(?!(aud|cad|sgd))", re.I)
            )
        else:
            res.append(re.compile(f"{curr_expr} ?{number_group_regex}", re.I))
        res.append(re.compile(f"{number_group_regex} ?{curr_expr}", re.I))
    return res


price_regexes = {
    **{
        curr: generate_curr_regexes(curr_exprs)
        for curr, curr_exprs in currencies.items()
    },
}

no_curr_price_regexes = [
    re.compile(f"{number_group_regex} ?shipped", re.I),
    re.compile(rf"{number_group_regex} ?\+ ?ship", re.I),
]


class PriceTag(BaseModel):
    currency: Optional[Currency]
    amount: float
    striked: bool

    @validator("amount", pre=True)
    def replace_comma(cls, value):
        if isinstance(value, str):
            return value.replace(",", ".")
        else:
            return value

    class Config:
        extra = "forbid"


def find_prices_in_text(text: Text) -> list[PriceTag]:
    res = []
    for curr, regexes in price_regexes.items():
        for regex in regexes:
            matches = regex.finditer(text.text)
            res.extend(
                PriceTag(
                    currency=curr,
                    amount=match.group("price"),
                    striked=text.is_striked(),
                )
                for match in matches
            )
    if not res:
        for regex in no_curr_price_regexes:
            matches = regex.finditer(text.text)
            res.extend(
                PriceTag(
                    currency=None,
                    amount=match.group("price"),  # type: ignore
                    striked=text.is_striked(),
                )
                for match in matches
            )

    return res


def find_price_wo_curr_in_text(text: Text, min_amount=10, max_amount=10000):
    """Find numbers in text. If a number is more than min_amount, consider it as unitless price."""
    number_only_regex = f"(?<![a-z0-9-])({number_group_regex})(?![a-z.,0-9])"
    matches = re.finditer(number_only_regex, text.text, flags=re.IGNORECASE)
    res = []
    for match in matches:
        price_tag = PriceTag(
            currency=None, amount=match.group("price"), striked=text.is_striked()  # type: ignore
        )
        if price_tag.amount >= min_amount and price_tag.amount < max_amount:
            res.append(price_tag)
    return res


def find_sold_token_in_text(text: Text):
    # sold followed by some letter is not matched, except when the letter is `d`
    # (because sometimes people write soldd)
    return [
        (
            bool(re.search("sold(?![a-ce-z])", text.text.lower()))
            or "traded" in text.text.lower()
        )
    ]


def find_price_token_in_text(text: Text):
    text_lower = text.text.lower()
    return [
        (
            "price" in text_lower
            or "want" in text_lower
            or "asking" in text_lower
            or "usd" in text_lower
            or "cost" in text_lower
            or "pricing" in text_lower
        )
    ]
