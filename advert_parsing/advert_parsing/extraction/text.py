from advert_parsing.markdown_parser import (
    Text, Listing, Table, Paragraph,
    Mdast, MdElement, Listing,
    md_to_ast, Root, ListItem, LineBreak, Heading, Parent
)
from advert_parsing.markdown_parser.utils import find_in_tree, split_paragraph

from advert_parsing.classification.prices import (
    find_prices_in_text, find_price_wo_curr_in_text, find_sold_token_in_text
)
from .extracted_item import ExtractedItem



def remove_tables(ast: MdElement):
    """Returns same AST, without the tables.

    Useful so that tables do not mess with the number of prices.
    """
    if isinstance(ast, Parent):
       return ast.copy(update={"children":[
           remove_tables(child) for child in ast.children
           if not isinstance(child, Table)
       ]})
    else:
        return ast

def extracts_items_from_text(ast: MdElement, res: list[ExtractedItem]):
    prices = find_in_tree(find_prices_in_text)(ast)
    if len(prices) == 0:
        return
    if len(prices) == 1:
        res.append(ExtractedItem(ast=ast,prices=prices,images=[]))
        return
    if isinstance(ast, Paragraph):
        split_parag = split_paragraph(ast)
        if len(split_parag) > 1:
            for item in split_parag:
                extracts_items_from_text(item, res)
        else:
            res.append(ExtractedItem(ast=ast,prices=prices,images=[]))
    elif isinstance(ast, Parent):
        for child in ast.children:
            extracts_items_from_text(child, res)
    else:
        res.append(ExtractedItem(ast=ast,prices=prices,images=[]))

def extract_text_items(ast: MdElement):
    res = []
    ast_no_table = remove_tables(ast)
    extracts_items_from_text(ast_no_table, res)
    return res

