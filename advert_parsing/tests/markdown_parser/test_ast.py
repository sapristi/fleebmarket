from advert_parsing.markdown_parser.md_ast import (
    Root,
    Paragraph, Text,  Heading, Listing, Table, 
)

from advert_parsing.markdown_parser.ast_renderer import (
    xml_to_ast,
    collapse_ast,
)

def test_collapse():
    ast = Root(children=[
        Paragraph(children=[Text(text='a')])
    ])
    assert collapse_ast(ast, []) == ast

    ast = Paragraph(children=[Text(text='a'), Text(text='b')])
    assert collapse_ast(ast, []) == Paragraph(children=[Text(text='a b')])
