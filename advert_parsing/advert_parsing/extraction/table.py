from typing import Iterable
import more_itertools

from advert_parsing.markdown_parser import (
    Text, Listing, Table, Paragraph,
    Mdast, MdElement, Listing,
    md_to_ast, Root, ListItem
)
from advert_parsing.markdown_parser.utils import find_in_tree, extract_tables
from advert_parsing.classification.table import ItemsTable, combined_classif
from advert_parsing.classification.prices import (
    find_prices_in_text, find_price_wo_curr_in_text, find_sold_token_in_text
)
from .extracted_item import ExtractedItem
from advert_parsing.dataframe import DataFrame


def extract_items_from_table(table: Table, classif: ItemsTable) -> Iterable[ExtractedItem]:
    if classif.has_header:
        header = table.rows[0]
        rows = table.rows[1:]
        make_ast = lambda row: Table(rows=[header, row])
    else:
        rows = table.rows
        def make_ast_(row):
            return Listing(
                children=[
                    ListItem(children=cell.children)
                    for cell in row
                    if cell is not None
                ]
            )
        make_ast = make_ast_

    for row in rows:
        ast = make_ast(row)
        price_cells = [row[i] for i in classif.price_cols]
        prices = [
            price
            for cell in price_cells
            for price in find_in_tree(find_prices_in_text)(cell)
        ]
        if len(prices) == 0:
            prices = [
                price
                for cell in price_cells
                for price in find_in_tree(find_price_wo_curr_in_text)(cell)
            ]
        images = []
        yield ExtractedItem(ast=ast, prices=prices, images=images)


def extract_table_items(advert_ast: MdElement) -> Iterable[ExtractedItem]:
    tables = extract_tables(advert_ast)
    for table in tables:
        table_df = DataFrame(table.rows)
        classif = combined_classif(table_df)
        if not isinstance(classif, ItemsTable):
            continue
        for item in extract_items_from_table(table, classif):
            yield item

