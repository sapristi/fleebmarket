import xml.etree.ElementTree as ET

import pytest
from advert_parsing.markdown_parser.ast_renderer import xml_to_ast
from advert_parsing.markdown_parser.md_ast import (
    Cell,
    Heading,
    Listing,
    ListItem,
    Paragraph,
    Root,
    StyleValue,
    Table,
    Text,
)
from advert_parsing.markdown_parser.utils import get_diff, md_wordcount
from advert_parsing.markdown_parser.xml_renderer import parse_md_to_xml
from devtools import debug


def CellShortcut(*values):
    return Cell(children=[Text(text=value) for value in values])


def ListingShortcut(*values):
    return Listing(children=[ListItem(children=[Text(text=value)]) for value in values])


def ListItemShortcut(*values):
    return ListItem(children=[Text(text=value) for value in values])


test_cases = {
    "list": (
        """
  - a
  - b""",
        Root(children=[ListingShortcut("a", "b")]),
    ),
    "list_w_markup": (
        """
 * a *b* c.
 * *d*
 * ~~e~~ f""",
        Root(
            children=[
                Listing(
                    children=[
                        ListItemShortcut("a b c."),
                        ListItemShortcut("d"),
                        ListItem(
                            children=[
                                Text(text="e", styles={StyleValue.STRIKE}),
                                Text(text="f"),
                            ]
                        ),
                    ]
                )
            ]
        ),
    ),
    "blockquote": (
        """
> a
> b
""",
        Root(children=[Paragraph(children=[Text(text="a b")])]),
    ),
    "inline_links": (
        """
[a](bar) b [c](bar)
""",
        Root(children=[Paragraph(children=[Text(text="a b c")])]),
    ),
    "inline_code": (
        """a `b`""",
        Root(children=[Paragraph(children=[Text(text="a b")])]),
    ),
    "list like strings": (
        """a

    *   b
""",
        Root(
            children=[
                Paragraph(children=[Text(text="a")]),
                Paragraph(children=[Text(text="*   b")]),
            ]
        ),
    ),
    "multi_line_format": (
        """
a **b
c** d
""",
        Root(
            children=[
                Paragraph(
                    children=[
                        Text(text="a"),
                        Text(text="b", styles={StyleValue.STRONG}),
                        Text(text="c", styles={StyleValue.STRONG}),
                        Text(text="d"),
                    ]
                )
            ]
        ),
    ),
    "pre blocks and nested lists": (
        """
   - a
   - b

     c

         d

     f

   - g

       - h
       - j
""",
        Root(
            children=[
                Listing(
                    children=[
                        ListItemShortcut("a"),
                        ListItem(
                            children=[
                                Paragraph(
                                    children=[
                                        Text(text="b"),
                                    ]
                                ),
                                Paragraph(
                                    children=[
                                        Text(text="c"),
                                    ]
                                ),
                                Paragraph(
                                    children=[
                                        Text(text="d"),
                                    ]
                                ),
                                Paragraph(
                                    children=[
                                        Text(text="f"),
                                    ]
                                ),
                            ]
                        ),
                        ListItem(
                            children=[
                                Paragraph(
                                    children=[
                                        Text(text="g"),
                                    ]
                                ),
                                ListingShortcut("h", "j"),
                            ]
                        ),
                    ]
                )
            ]
        ),
    ),
}


@pytest.mark.parametrize("md,expected", test_cases.values())
def test_basic_md(md, expected):
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)
    assert ast == expected


def cells_of_list(l):
    return [
        Cell(children=item) if isinstance(item, list) else Cell(children=[item])
        for item in l
    ]


tables_md = [
    """
| a | b | c |
|---|---|---|
| d | e | f |
""",
    """
| a | b | c |
|---|---|---|
 d | e | f |
""",
    """
| a | b | c |
|---|---|---|
| d | e | f 
""",
    """
| a | b | c |
|---|---|---|
 d | e | f 
""",
    """
 a | b | c 
---|---|---
 d | e | f 
""",
]
tables_ast = Root(
    children=[
        Table(
            rows=[
                [CellShortcut("a"), CellShortcut("b"), CellShortcut("c")],
                [CellShortcut("d"), CellShortcut("e"), CellShortcut("f")],
            ]
        )
    ]
)

table_test_cases = zip(tables_md, [tables_ast] * len(tables_md))


@pytest.mark.parametrize("md,expected", table_test_cases)
def test_tables(md, expected):
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)

    assert ast == expected


def test_custom_1():
    md = """https://imgur.com/a/lMBDhmL
Asking 315+Shipping, currently been mounted for 5 days now, 1 1/2 hours clocked of valorant.
NC-27587 >>>>SOLD<<<<"""
    expected = Root(
        children=[
            Paragraph(
                children=[
                    Text(
                        text="https://imgur.com/a/lMBDhmL Asking 315+Shipping, currently been mounted for 5 days now, 1 1/2 hours clocked of valorant. NC-27587 SOLD"
                    )
                ]
            )
        ]
    )
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)

    assert ast == expected


def test_custom_2():
    md = """[>SEND ME A PM HERE<](https://url.com)"""
    expected = Root(children=[Paragraph(children=[Text(text="SEND ME A PM HERE")])])
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)

    assert ast == expected


def test_custom_3():
    md = """[\\>SEND ME A PM HERE<](https://url.com)"""
    expected = Root(children=[Paragraph(children=[Text(text="SEND ME A PM HERE")])])
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)

    assert ast == expected


def test_custom_4():
    md = """
 a | b 
---|---
 d | e 
    """
    expected = Root(
        children=[
            Table(
                rows=[
                    [CellShortcut("a"), CellShortcut("b")],
                    [CellShortcut("d"), CellShortcut("e")],
                ]
            )
        ]
    )
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)

    assert ast == expected


def test_custom_5():
    md = """
##title:
 a | b 
    -|-
 d | e 
    """
    expected = Root(
        children=[
            Heading(children=[Text(text="title:")], level=2),
            Table(
                rows=[
                    [CellShortcut("a"), CellShortcut("b")],
                    [CellShortcut("d"), CellShortcut("e")],
                ]
            ),
        ]
    )
    xml = parse_md_to_xml(md)
    ET.dump(xml)
    ast = xml_to_ast(xml)
    if diff := get_diff(ast, expected):
        debug(MD=md, **diff)

    assert ast == expected


@pytest.mark.parametrize("md,expected", test_cases.values())
def test_wordcount(md, expected):
    xml = parse_md_to_xml(md)
    ast = xml_to_ast(xml)
    wc = md_wordcount(ast)


def test_parse_adverts(adverts_md):
    for name, md in adverts_md:
        xml = parse_md_to_xml(md)
        ast = xml_to_ast(xml)
