from advert_parsing.markdown_parser import md_to_ast
from advert_parsing.extraction.extracted_item import ExtractedItem
from advert_parsing.extraction.text import  extract_text_items
from advert_parsing.extraction.table import  extract_table_items



def parse(md_str: str) -> list[ExtractedItem]:

    ast = md_to_ast(md_str)
    text_items = list(extract_text_items(ast))
    table_items = list(extract_table_items(ast))

    return [
        *text_items,
        *table_items
    ]
