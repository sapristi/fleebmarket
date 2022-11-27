import more_itertools

from .md_ast import (
    Cell,
    Heading,
    LineBreak,
    Link,
    Listing,
    ListItem,
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


def split_paragraph(paragraph: Paragraph) -> list[Paragraph]:
    """Splits a Paragraph into multiple paragraphs, by Linebreak"""
    res = []
    current_res = []
    for child in paragraph.children:
        if isinstance(child, LineBreak):
            if current_res:
                res.append(Paragraph(children=current_res))
                current_res = []
        else:
            current_res.append(child)
    if current_res:
        res.append(Paragraph(children=current_res))
    return res


def md_wordcount(item: MdElement):
    if isinstance(item, Parent):
        return sum(map(md_wordcount, item.children))
    elif isinstance(item, Table):
        return sum(md_wordcount(cell) for row in item.rows for cell in row)
    elif isinstance(item, Text):
        return len(item.text.split())
    elif isinstance(item, ThematicBreak) or isinstance(item, LineBreak):
        return 0
    else:
        raise Exception(f"Unkown element: {item.__class__} ({item})")


def get_diff(ast1, ast2):
    if ast1.__class__ != ast2.__class__:
        return {"problem": "different classes", "got": ast1, "expected": ast2}
    if isinstance(ast1, Parent):
        if len(ast1.children) != len(ast2.children):
            return {
                "problem": "not same number of children",
                "got": ast1.children,
                "expected": ast2.children,
            }
        children_zip = zip(ast1.children, ast2.children)
        for child1, child2 in children_zip:
            diff = get_diff(child1, child2)
            if diff is not None:
                return diff

    if ast1 != ast2:
        return {"problem": "different values", "got": ast1, "expected": ast2}
    return None


def find_in_tree(find_function):
    def inner(cell):
        if (
            cell is None
            or isinstance(cell, LineBreak)
            or isinstance(cell, ThematicBreak)
        ):
            return []
        if isinstance(cell, Text):
            return find_function(cell)
        else:
            return list(
                more_itertools.collapse(
                    [find_in_tree(find_function)(child) for child in cell.children],
                    levels=1,
                )
            )

    return inner


def clean_table(table: Table):
    ok_rows = []
    for row in table.rows:
        if any(row):
            ok_rows.append(row)

    return Table(rows=ok_rows)


def extract_tables(item: MdElement) -> list[Table]:
    if isinstance(item, Table):
        return [item]
    elif isinstance(item, Listing) or isinstance(item, Root):
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
