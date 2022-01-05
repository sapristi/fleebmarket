from advert_parsing.markdown_parser import Table, Text, Root, Paragraph, Listing, ListItem
from advert_parsing.classification.table import clean_table, extract_tables

def test_clean_table():
    res = clean_table(Table(rows=[
        [Text(text='ok'), None],
        [None, None]
    ]))
    assert res == Table(rows=[[Text(text='ok'), None]])

def test_extract_tables():
    ast = Root(children=[
        Table(rows=[]),
        Listing(children=[
            ListItem(children=[Text(text=""), Table(rows=[])])
        ])
    ])
    assert len(extract_tables(ast)) == 2
