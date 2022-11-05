from advert_parsing.classification.prices import (
    find_price_wo_curr_in_text,
    find_prices_in_text,
    find_sold_token_in_text,
)
from advert_parsing.markdown_parser import (
    Heading,
    LineBreak,
    Listing,
    ListItem,
    Mdast,
    MdElement,
    Paragraph,
    Parent,
    Root,
    Table,
    Text,
    md_to_ast,
    ThematicBreak,
    StyleValue
)
from advert_parsing.markdown_parser.utils import find_in_tree, split_paragraph

from .extracted_item import ExtractedItem


def remove_tables(ast):
    """Returns same AST, without the tables.

    Useful so that tables do not mess with the number of prices.
    """
    if isinstance(ast, Parent):
        return ast.copy(
            update={
                "children": [
                    remove_tables(child)
                    for child in ast.children
                    if not isinstance(child, Table)
                ]
            }
        )
    else:
        return ast


def is_heading_or_bold_text(item):
    return isinstance(item, Heading) or (
        isinstance(item, Paragraph)
        and len(item.children) == 1
        and isinstance(item.children[0], Text)
        and StyleValue.STRONG in item.children[0].styles
    )

def split_ast(tree: Root) -> list[Root]:
    """Split the AST (by headings, breaks, etc)"""
    res = []
    current_children = []
    for child in tree.children:
        if isinstance(child, ThematicBreak):
            res.append(Root(children=current_children))
            current_children = []
        if is_heading_or_bold_text(child):
            res.append(Root(children=current_children))
            current_children = [child]
        else:
            current_children.append(child)
    res.append(Root(children=current_children))
    return res


def get_nb_nodes_with_price(ast: MdElement) -> int:
    """We want to count the number of Paragraph nodes with prices in them"""
    if isinstance(ast, Paragraph) or isinstance(ast, ListItem):
        prices = find_in_tree(find_prices_in_text)(ast)
        return 1 if len(prices) > 0 else 0

    elif isinstance(ast, Parent):
        return sum(
            get_nb_nodes_with_price(child) for child in ast.children
        )
    else:
        return 0


def extract_items_from_text(ast: MdElement, res: list[ExtractedItem] | None = None):
    if res is None:
        res = []
    prices = find_in_tree(find_prices_in_text)(ast)
    nb_nodes_with_price = get_nb_nodes_with_price(ast)
    if nb_nodes_with_price == 0:
        return res
    if nb_nodes_with_price == 1:
        res.append(ExtractedItem(ast=ast, prices=prices, images=[]))
        return res
    if isinstance(ast, Paragraph):
        split_parag = split_paragraph(ast)
        if len(split_parag) > 1:
            for item in split_parag:
                extract_items_from_text(item, res)
        else:
            res.append(ExtractedItem(ast=ast, prices=prices, images=[]))
    elif isinstance(ast, Parent):
        for child in ast.children:
            extract_items_from_text(child, res)
    else:
        res.append(ExtractedItem(ast=ast, prices=prices, images=[]))
    return res


def extract_text_items(ast: Root):
    ast_no_table = remove_tables(ast)
    asts = split_ast(ast_no_table)

    return [
        item for ast in asts
        for item in extract_items_from_text(ast)
    ]
