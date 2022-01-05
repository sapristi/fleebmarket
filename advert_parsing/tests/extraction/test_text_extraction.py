from advert_parsing.markdown_parser import (
    Text, Listing, ListItem, Table, Paragraph,
    Mdast, MdElement, Listing,
    md_to_ast, Root
)
from advert_parsing.extraction.text import  extract_text_items


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
        print(item)
    assert len(items) == 2


def test_text_extraction2():
    md_str = """

[timestamp](https://imgur.com/a/ZZvUW5M)

Noxary 268.2:

\-63.5g spring swapped gateron ink blacks, with deskey films and lubed with krytox 205g0/105 on springs (5mm pc plate)

\-alpaca on fn and right alt, tangie on spacebar

\-comes with a extra desoldered but fully working pcb

\-there is a patina on the weight (see pics)

Asking 400 SHIPPED CONUS
    """
    ast = md_to_ast(md_str)
    items = list(extract_text_items(ast))
    for item in items:
        print(item)
    assert len(items) == 1

