from advert_parsing.extraction.text import extract_text_items
from advert_parsing.markdown_parser import (
    Listing,
    ListItem,
    Mdast,
    MdElement,
    Paragraph,
    Root,
    Table,
    Text,
    md_to_ast,
)


def test_text_extraction1():
    md_str = """
[Timestamp first](https://imgur.com/a/wxO1hy8)

Have my end game build in place and need to pass on these parts to free up a little extra cash for Christmas gifts. Really would prefer to sell it as a complete bundle, so priority will be given to a buyer willing to take all of it. After checking on the value of everything and knocking a few bucks off each item, it all summed up to $268. I'm willing to let the whole bundle go for **$200 net to me**, and I'll cover shipping. Posting valuation below.

* GMK Apollo Novelties - $120
* JWK Black Linears (90 switches at $2.70 for 10) - $20
* JWK Black Tactiles (90 switches at $2.70 for 10) - $20
* Kalih Polia Switches (110 at $6 for 10) - $60
* GMMK Pro Polycarbonate Plate - $10
* GMMK Pro Aluminum Plate - $10
* Rotary Nobs (3 total) - $15
* Porcelain Blues (10 53g and 10 62g) - $8
* PCB Soulmate - $5
    """

    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))
    # for item in items:
    #     print(item)
    assert len(items) == 10


def test_text_extraction2():
    md_str = """
Hey Mechmarket!

I’m trying to find these Pokémon artisans a new home. Price includes shipping (US Only). Comment first, then shoot a PM!

https://imgur.com/a/YfAARI8

######BOB Gengar:

• Bulbasaur - $85

######Rath Poliwrath:

• OG Blue (w/ Red blood drops) - $50

Thanks in advance!
(Sorry about formatting, on mobile
    """
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))
    for item in items:
        print(item.sold)
    assert len(items) == 2


def test_text_extraction3():
    md_str = """

[timestamp](https://imgur.com/a/ZZvUW5M)

Noxary 268.2:

\\-63.5g spring swapped gateron ink blacks, with deskey films and lubed with krytox 205g0/105 on springs (5mm pc plate)

\\-alpaca on fn and right alt, tangie on spacebar

\\-comes with a extra desoldered but fully working pcb

\\-there is a patina on the weight (see pics)

Asking 400 SHIPPED CONUS
    """
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))
    for item in items:
        print(item)
    assert len(items) == 1


def test_text_extraction_remove_table():
    md_str = """
 Timestamps/Pictures: [https://imgur.com/a/8s1pwDh](https://imgur.com/a/8s1pwDh)

 &#x200B;

 Rama Jules: 380 USD shipped- Kuro/Oro- Hotswap- Extra POM Plate- Stupidfish Foam- Assembled once, in almost new condition. no flaws

 ~~GMK Dark: 400 USD shipped- new, only opened to inspect- base~~ SOLD

 ~~GMK Olivia Dark: 350 USD shipped- new, only opened to inspect- base~~ SOLD

 GMK Minimal R2: 150 USD shipped- new, sealed- base

 JTK Night Sakura: 180 USD shipped- new- base, latin alphas

 Akko Black and Pink Keycaps:- new- 50 USD shipped

 Artisans-

|Rama Vaporwave: 100 USD shipped|Rama Vaporwave: 100 USD shipped|Rama Hiragana: 50 USD shipped (mounts slightly crooked)|~~Rama Thermal Moon: 60 USD shipped~~ SOLD|
|:-|:-|:-|:-|
|~~Rama Stealth: 100 USD shipped~~ SOLD|Rama Masterpiece: 100 USD shipped|Rama Dolch: 50 USD shipped|~~Thok Agent01: 75 USD shipped~~ SOLD|
|~~Rama First Love: 100 USD shipped~~ SOLD|Monokei x CYSM Keyby: 100 USD shipped|~~Rama Ivory: 60 USD shipped~~ SOLD|Stacchio Bois Teal: 50 USD shipped|
|Thok Queen: 75 USD shipped|Thok Ace: 60 USD shipped|Thok Ace: 60 USD shipped||

 Please pm and no chats. Thanks

 Edit: all uploaded/ updating sold items

    """
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))
    for item in items:
        print(item)
    assert len(items) == 6


def test_text_extraction_remove_table_minimal():
    md_str = """
|Rama Vaporwave: 100 USD shipped|Rama Vaporwave: 100 USD shipped|Rama Hiragana: 50 USD shipped (mounts slightly crooked)|~~Rama Thermal Moon: 60 USD shipped~~ SOLD|
|:-|:-|:-|:-|
|~~Rama Stealth: 100 USD shipped~~ SOLD|Rama Masterpiece: 100 USD shipped|Rama Dolch: 50 USD shipped|~~Thok Agent01: 75 USD shipped~~ SOLD|
|~~Rama First Love: 100 USD shipped~~ SOLD|Monokei x CYSM Keyby: 100 USD shipped|~~Rama Ivory: 60 USD shipped~~ SOLD|Stacchio Bois Teal: 50 USD shipped|
    """
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))
    assert len(items) == 0



def test_text_extraction_separators_zero_space(advert_md):
    md_str = advert_md("advert_with_zero_width_spaces")
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))

    assert len(items) == 14
    assert len(items[0].ast.children) == 10  # make sure we have more than a single line

def test_text_extraction_separators_hline(advert_md):
    md_str = advert_md("advert_with_separators.md")
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))

    assert len(items) == 2
    assert len(items[0].ast.children) == 3  # make sure we have more than a single line

def test_text_extraction_separators_bold_text(advert_md):
    md_str = advert_md("advert_with_headings_01.md")
    ast = md_to_ast(md_str)
    # for child in ast.children:
    #     print(child)
    items = list(extract_text_items(ast))
    assert len(items) == 5
    assert len(items[0].ast.children) == 2  # make sure we have more than a single line

