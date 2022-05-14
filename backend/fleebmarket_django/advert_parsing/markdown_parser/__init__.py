from .ast_renderer import xml_to_ast
from .md_ast import (
    Cell,
    Heading,
    LineBreak,
    Listing,
    ListItem,
    Mdast,
    MdElement,
    Paragraph,
    Parent,
    Root,
    Style,
    StyleValue,
    Table,
    Text,
    ThematicBreak,
)
from .xml_renderer import parse_md_to_xml


def md_to_ast(md) -> MdElement:
    xml = parse_md_to_xml(md)
    return xml_to_ast(xml)
