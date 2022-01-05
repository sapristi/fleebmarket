from .md_ast import (
    Root, Text, Table, Cell, Paragraph, LineBreak, ThematicBreak,
    Listing, ListItem, Heading, Style, StyleValue,
    Mdast, MdElement, Parent
)
from .ast_renderer import xml_to_ast
from .xml_renderer import parse_md_to_xml

def md_to_ast(md) -> MdElement:
    xml = parse_md_to_xml(md)
    return xml_to_ast(xml)
