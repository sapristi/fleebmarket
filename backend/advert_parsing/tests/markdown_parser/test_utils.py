from advert_parsing.markdown_parser import LineBreak, Listing, ListItem, Paragraph, Text
from advert_parsing.markdown_parser.utils import split_paragraph


def test_split_paragraph():
    t = Text(text="something")
    p1 = Paragraph(children=[t, t, t])
    assert split_paragraph(p1) == [p1]
    p2 = Paragraph(children=[t, LineBreak(), t])
    assert split_paragraph(p2) == [
        Paragraph(children=[t]),
        Paragraph(children=[t]),
    ]
