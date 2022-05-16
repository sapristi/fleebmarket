from advert_parsing.extraction.table import extract_table_items
from advert_parsing.markdown_parser import (
    Listing,
    Mdast,
    MdElement,
    Paragraph,
    Root,
    Table,
    Text,
    md_to_ast,
)


def test_extraction_from_tables(adverts_md):
    for name, md in adverts_md:
        print("Parsing", name)
        ast = md_to_ast(md)
        items = list(extract_table_items(ast))
        print("From", name, len(items))
        for item in items:
            print(" -", item)


def test_extraction_table_base_1():
    md_str = """
| Description                                          | Price   | Notes                                    |
|------------------------------------------------------|---------|------------------------------------------|
| Rama Works KARA SEQ1 (ICED) + extra alu plate (MIST) | 200 EUR | Excellent condition, no dings/scratches. |
| Rama Works M60-A SEQ2 (MOON STEALTH)                 | 600 EUR | Excellent condition, no dings/scratches. |
| Rama Works M60-A extra PVD brass back weight (MOON)  | 100 EUR | Excellent condition, no dings/scratches  |
| Rama Works internal dampener (MOON)                  | 50 EUR  | Excellent condition                      |
| Rama Works internal brass weight (MOON)              | 80 EUR  | Excellent condition                      |
        """
    ast = md_to_ast(md_str)
    items = list(extract_table_items(ast))

    assert len(items) == 5
    print(items)


def test_extraction_table_base_2():
    md_str = """
| Zero Sky Cyber Marshall - Lazurite Blue     | $90 |
|---------------------------------------------|-----|
| Zero Sky Cyber Marshall - Lazurite White    | $90 |
| Krakenkap Cacodemon - Lazurite              | $40 |
| Krakencap Corrupted Owl - Lazurite          | $40 |
| Zero Sky Cyber Marshall - GMK Dreaming Bird | $90 |
| Zero Sky Argos - GMK Dreaming Bird          | $90 |
| Krapshop Catto19 Lazurite Calcite (White)   | $50 |
| Gukong Lazurite                             | $45 |
        """

    ast = md_to_ast(md_str)
    items = list(extract_table_items(ast))
    assert len(items) == 8


def test_extraction_table_base_3():
    md_str = """
Maker | Sculpt | Colorway  
:--:|:--:|:--:  
Alpha | Keypora | Amaririsu ($175), Clozer Night (trades), Ma Nuts ($175)
Artkey | Devourer | Gorgon ($150)
Artkey | Amu | Necropolis ($80), Nori ($80)
        """

    ast = md_to_ast(md_str)
    items = list(extract_table_items(ast))
    assert len(items) == 3


def test_extraction_table_base_4():
    md_str = """
Maker | Sculpt | Colorway  
:--:|:--:|:--:  
Alpha | Keypora | Strangelove
Booper | Cosmo v2 | Garnet
GAF | Grimace v1 | Any colorway
        """

    ast = md_to_ast(md_str)
    items = list(extract_table_items(ast))
    assert len(items) == 0


def test_extraction_table_base_5():
    md_str = """
|Rama Vaporwave: 100 USD shipped|Rama Vaporwave: 100 USD shipped|Rama Hiragana: 50 USD shipped (mounts slightly crooked)|~~Rama Thermal Moon: 60 USD shipped~~ SOLD|
|:-|:-|:-|:-|
|~~Rama Stealth: 100 USD shipped~~ SOLD|Rama Masterpiece: 100 USD shipped|Rama Dolch: 50 USD shipped|~~Thok Agent01: 75 USD shipped~~ SOLD|
|~~Rama First Love: 100 USD shipped~~ SOLD|Monokei x CYSM Keyby: 100 USD shipped|~~Rama Ivory: 60 USD shipped~~ SOLD|Stacchio Bois Teal: 50 USD shipped|
    """
    ast = md_to_ast(md_str)

    items = list(extract_table_items(ast))
    assert len(items) == 0
