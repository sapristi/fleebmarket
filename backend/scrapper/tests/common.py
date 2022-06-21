from dataclasses import dataclass

ok_title = "[RU][H] Supa Dupa Pre-Assembled Corne PCBs [W] Paypal"
ko_title = "HEERE[W] Supa Dupa Pre-Assembled Corne PCBs [W] Paypal"

body = """[Timestamp](https://imgur.com/a/lqGir8t)\n\n&#x200B;\n\nSA-P Snow Cap:\n\n\\-Alphas-60% Icon kit-7u Spacebar-R1:Delete (1u)-R3: 2x Windows Icon (1u), 2x Alt Icon (1.5U)-R4: Shift Icon(1.75u)\n\nLoved the sound and feel of this set, used for a few weeks, just decided I prefer KAT to SA so this set sees little use. Cost about $120 for all brand new -  $75\n\n&#x200B;\n\nJelly Key:\n\nThe Rehabilitation of Lost Cities artisan keycaps - Amazil City, SA R3 - 2.25\n\nPurchased this for the SA Set, no use for it now, only mounted once, just looking to get back what I paid - $65"""


@dataclass
class PrawAuthorMock:
    name: str


@dataclass
class PrawSubmissionMock:
    id: str
    author: PrawAuthorMock
    title: str
    link_flair_text: str
    selftext: str
    created_utc: int
