from search_app.models.parse import Link, parse_mechmarket_body

body_1 = """
-Discounted prices-  https://imgur.com/a/fbsRAYv
"""


def test_parse_text_links():
    res = parse_mechmarket_body(body_1)
    assert res.links == [Link(href="https://imgur.com/a/fbsRAYv", title=None)]


body_2 = """
-Discounted prices-  https://imgur.com/a/fbsRAYv
[test](https://imgur.com/a/fbsRAYv)
"""


def test_parse_text_links_2():
    res = parse_mechmarket_body(body_2)
    assert res.links == [Link(href="https://imgur.com/a/fbsRAYv", title="test")]
