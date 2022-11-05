import os
from pathlib import Path
from typing import Tuple

import pytest

DATA_DIR = Path(__file__).parent / "data"


@pytest.fixture(scope="session")
def adverts_md() -> list[Tuple[str, str]]:
    res = []
    md_dir = DATA_DIR / "adverts_md"
    for filename in md_dir.iterdir():
        if not filename.is_file():
            continue
        res.append((str(filename.name), filename.read_text()))
    return res

@pytest.fixture(scope="session")
def advert_md():
    def inner(name):
        md_file = DATA_DIR / "adverts_md" / name
        return md_file.read_text()
    return inner
