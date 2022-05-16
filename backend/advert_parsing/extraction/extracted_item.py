from typing import Optional

from advert_parsing.classification.prices import PriceTag, find_sold_token_in_text

# for some reason necessary for upate_forward_ref to work
from advert_parsing.markdown_parser.md_ast import *
from advert_parsing.markdown_parser.md_ast import MdElement
from advert_parsing.markdown_parser.utils import find_in_tree
from pydantic import BaseModel


class ExtractedItem(BaseModel):
    class Config:
        extra = "forbid"
        allow_mutation = False

    ast: MdElement
    prices: list[PriceTag]
    images: list[str]

    @property
    def sold(self) -> bool:
        if all((price.striked for price in self.prices)):
            return True
        sold_tokens = find_in_tree(find_sold_token_in_text)(self.ast)
        return any(sold_tokens)

    @property
    def relevant_price(self) -> Optional[PriceTag]:
        # TODO: many things to improve here, but here we go
        if len(self.prices) == 0:
            return None
        max_amount = 0
        max_price = None
        for price in self.prices:
            if price.striked and not self.sold:
                continue
            if price.amount > max_amount:
                max_amount = price.amount
                max_price = price
        return max_price


ExtractedItem.update_forward_refs()
