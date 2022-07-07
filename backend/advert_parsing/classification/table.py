from dataclasses import dataclass
from typing import Optional, Union

import more_itertools
from advert_parsing.dataframe import DataFrame
from advert_parsing.markdown_parser.md_ast import MdElement, Parent, Table, Text
from pydantic import BaseModel

from .prices import (
    find_price_token_in_text,
    find_price_wo_curr_in_text,
    find_prices_in_text,
)


def clean_table(table: Table):
    ok_rows = []
    for row in table.rows:
        if any(row):
            ok_rows.append(row)

    return Table(rows=ok_rows)


def extract_tables(item: MdElement):
    if isinstance(item, Table):
        return [item]
    elif isinstance(item, Parent):
        extracted_tables_lists = [extract_tables(child) for child in item.children]
        tables = [
            clean_table(t)
            for tables in extracted_tables_lists
            for t in tables
            if tables is not None
        ]
        return tables
    else:
        return []


def find_in_cell(find_function):
    def inner(cell):
        if cell is None:
            return []
        if isinstance(cell, Text):
            return find_function(cell)
        else:
            return list(
                more_itertools.collapse(
                    [find_in_cell(find_function)(child) for child in cell.children],
                    levels=1,
                )
            )

    return inner


class FoundPrices(BaseModel):
    col_index: int
    nb_found: int


@dataclass
class ArtisanTable:
    pass


class ItemsTable(BaseModel):
    price_cols: list[int]
    has_header: Optional[bool] = None


@dataclass
class Failure:
    """Failure to classify"""

    reason: str


@dataclass
class NotRelevant:
    """Table does not contain anything usefull"""

    reason: str


TableClassification = Union[NotRelevant, ItemsTable, ArtisanTable, Failure]


def header_cell_with_price(cell):
    if cell is None:
        return False
    price_tokens = find_in_cell(find_price_token_in_text)(cell)
    price_tags = find_in_cell(find_prices_in_text)(cell)
    return sum(price_tokens) >= 1 and not price_tags


# TODO: we could also check for striked text, which would indicate it is not a header
def classify_with_header(df: DataFrame) -> Union[ItemsTable, Failure]:
    first_row = df.rows[0]
    cells_with_price = [header_cell_with_price(cell) for cell in first_row]
    price_header_indices = [
        i for i, is_price_header in enumerate(cells_with_price) if is_price_header
    ]
    if price_header_indices:
        return ItemsTable(price_cols=price_header_indices, has_header=True)
    return Failure("Cannot classify from header")


def make_bool_df(df: DataFrame, find_function):
    prices_df = df.applymap(find_in_cell(find_function))
    bool_df = prices_df.applymap(bool)
    return bool_df


def generate_repartion(bool_df: DataFrame) -> list[FoundPrices]:
    col_count = [sum(col) for col in bool_df.columns]
    repartition = []
    for i, value in enumerate(col_count):
        if value != 0:
            repartition.append(FoundPrices(nb_found=value, col_index=i))
    return sorted(repartition, key=lambda x: x.nb_found)


def classify_table_simple(df: DataFrame, find_function) -> TableClassification:
    nb_rows = len(df.rows)
    nb_cols = len(df.columns)

    bool_df = make_bool_df(df, find_function)
    repartition = generate_repartion(bool_df)

    if len(repartition) == 0:
        return NotRelevant(reason="No price")

    relevant_columns = [p for p in repartition if p.nb_found >= nb_rows / 2]
    if len(relevant_columns) == 0:
        return Failure(reason=f"Price: Not enough rows with price")

    if len(relevant_columns) == 1:
        value = relevant_columns[0]
        has_header = not any(bool_df.rows[0])
        return ItemsTable(price_cols=[value.col_index], has_header=has_header)

    if (
        (len(relevant_columns) == nb_cols)
        or (nb_cols > 3 and len(relevant_columns) >= nb_cols - 1)
        or (nb_cols > 4 and len(relevant_columns) >= nb_cols - 2)
    ):
        return ArtisanTable()

    return ItemsTable(price_cols=[value.col_index for value in relevant_columns])


def combined_classif(df: DataFrame) -> TableClassification:
    header_classif = classify_with_header(df)
    price_classif = classify_table_simple(df, find_prices_in_text)

    if not isinstance(price_classif, ItemsTable):
        price_classif_wocurr = classify_table_simple(df, find_price_wo_curr_in_text)
        if isinstance(price_classif_wocurr, ItemsTable):
            price_classif = price_classif_wocurr

    if isinstance(header_classif, ItemsTable):
        if isinstance(price_classif, ItemsTable):
            common_cols = set(header_classif.price_cols) & set(price_classif.price_cols)
            if len(common_cols) == 0:
                return Failure(reason="No common col between header and price classif")
            return ItemsTable(price_cols=list(common_cols), has_header=True)

        elif isinstance(price_classif, Failure):
            return header_classif

        else:
            return Failure(reason="different_classif")

    elif isinstance(header_classif, Failure):
        return price_classif
    else:
        raise Exception(f"Should not happen: header_classif {header_classif}")


# def combined_classif_py310(df):
#     header_classif = classify_with_header(df)

#     price_classif = classify_table_simple(df, find_prices_in_text)
#     if not isinstance(price_classif, ItemsTable):
#         price_classif_wocurr = classify_table_simple(df, find_price_wo_curr_in_text)
#         if isinstance(price_classif_wocurr, ItemsTable):
#             price_classif = price_classif_wocurr

#     match header_classif, price_classif:
#         case ItemsTable(price_cols=price_cols_1, has_header=_), ItemsTable(price_cols=price_cols_2):
#             common_cols = set(price_cols_1) & set(price_cols_2)
#             if len(common_cols) == 0:
#                 return Failure(reason="No common col between header and price classif")
#             return ItemsTable(price_cols=common_cols, has_header=True)

#         case ItemsTable(price_cols=price_cols, has_header=_), Failure(reason=_):
#             return ItemsTable(price_cols=price_cols, has_header=True)

#         case ItemsTable(price_cols=price_cols, has_header=_), ArtisanTable() | NotRelevant():
#             return Failure(reason="different_classif")

#         case Failure(reason=_), ItemsTable(price_cols=price_cols):
#             return ItemsTable(price_cols=price_cols, has_header=False)

#         case Failure(reason=_), _:
#             return price_classif

#         case _, _:
#             print(header_classif, price_classif)
#             raise
