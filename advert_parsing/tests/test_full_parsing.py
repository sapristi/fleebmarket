from advert_parsing import parse

def test_parse_adverts(adverts_md):
     for name, md in adverts_md:
         items = parse(md)
         for item in items:
             html = item.ast.to_html()
             print()
             print(html)
             assert len(item.prices) > 0 or "trades" in html
