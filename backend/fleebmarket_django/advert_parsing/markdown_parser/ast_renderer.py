from typing import TYPE_CHECKING

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
    Row,
    Style,
    StyleValue,
    Table,
    Text,
    ThematicBreak,
)

if TYPE_CHECKING:
    from xml.etree.ElementTree import Element


def xml_to_ast_raw(xml) -> MdElement:
    if xml.tag == "root":
        children = [xml_to_ast_raw(child) for child in xml]
        return Root(children=children)
    if xml.tag == "empty":
        return None
    if xml.tag == "text":
        if xml.text is None:
            return None
        return Text(text=xml.text)
    if xml.tag == "table":
        rows = [xml_to_ast_raw(row) for row in xml]
        return Table(rows=rows)
    if xml.tag == "cell":
        children = [xml_to_ast_raw(child) for child in xml]
        return Cell(children=children)
    if xml.tag == "row":
        cells = (xml_to_ast_raw(cell) for cell in xml)
        return Row(children=cells)
    if xml.tag == "p":
        children = [xml_to_ast_raw(child) for child in xml]
        return Paragraph(children=children)
    if xml.tag == "linebreak":
        return LineBreak()
    if xml.tag == "hrule":
        return ThematicBreak()
    if xml.tag == "list":
        children = [xml_to_ast_raw(child) for child in xml]
        return Listing(children=children)
    if xml.tag == "li":
        if xml.text:
            return ListItem(children=[Text(text=xml.text)])
        children = [xml_to_ast_raw(child) for child in xml]
        return ListItem(children=children)
    if xml.tag == "h":
        children = [xml_to_ast_raw(child) for child in xml]
        return Heading(children=children, level=xml.get("level"))
    if xml.tag == "striked":
        children = [xml_to_ast_raw(child) for child in xml]
        return Style(children=children, value=StyleValue.STRIKE)
    raise Exception(f"Unhandled xml tag: {xml.tag}[{xml.text}]")


def merge_styles(item: MdElement, styles: set[StyleValue]) -> MdElement:
    """Applies styles hints to text nodes. Does not remove Style nodes"""
    if isinstance(item, Text):
        return Text(text=item.text, styles=styles)
    elif isinstance(item, Style):
        # ignore non strike for now
        if item.value != StyleValue.STRIKE:
            return item.apply(lambda child: merge_styles(child, styles))
        return item.apply(lambda child: merge_styles(child, styles | {item.value}))
    if isinstance(item, Parent) or isinstance(item, Table):
        return item.apply(lambda child: merge_styles(child, styles))
    else:
        return item


def collapse_ast(ast: MdElement, classes_to_collapse):
    if isinstance(ast, Table) or isinstance(ast, Listing):
        return ast.apply(lambda item: collapse_ast(item, classes_to_collapse))

    if not isinstance(ast, Parent):
        return ast

    children = []
    for child in ast.children:
        if child is None:
            continue
        if isinstance(child, Style):
            children.extend(child.children)
        else:
            children.append(child)

    if len(children) == 0:
        return None

    if all(isinstance(node, Text) for node in children):
        if all(node.styles == children[0].styles for node in children):
            full_text = " ".join((node.text for node in children))
            if any(isinstance(ast, klass) for klass in classes_to_collapse):
                return Text(text=full_text, styles=children[0].styles)
            return ast.copy(
                update={"children": [Text(text=full_text, styles=children[0].styles)]}
            )

    return ast.copy(
        update={
            "children": [collapse_ast(child, classes_to_collapse) for child in children]
        }
    )


def xml_to_ast(
    xml: "Element", merge_style: bool = True, collapse: bool = False
) -> MdElement:
    classes_to_collapse = []
    ast = xml_to_ast_raw(xml)
    if merge_style:
        classes_to_collapse.append(Style)
        ast = merge_styles(ast, set())
    if collapse:
        classes_to_collapse.extend([Cell, ListItem])
    ast = collapse_ast(ast, classes_to_collapse)
    return ast
