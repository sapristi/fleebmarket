from advert_parsing.markdown_parser.ast_renderer import collapse_ast, xml_to_ast
from advert_parsing.markdown_parser.md_ast import (
    Heading,
    Listing,
    Paragraph,
    Root,
    Table,
    Text,
)


def test_collapse():
    ast = Root(children=[Paragraph(children=[Text(text="a")])])
    assert collapse_ast(ast, []) == ast

    ast = Paragraph(children=[Text(text="a"), Text(text="b")])
    assert collapse_ast(ast, []) == Paragraph(children=[Text(text="a b")])
