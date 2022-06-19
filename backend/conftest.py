from collections import defaultdict

import pytest
import search_app.meilisearch_utils


@pytest.fixture(autouse=True)
def meili_mock(monkeypatch):
    monkeypatch.setattr(
        search_app.meilisearch_utils.MAdvertsIndex, "name", "TEST_Adverts"
    )
    monkeypatch.setattr(
        search_app.meilisearch_utils.MAdvertsItemsIndex, "name", "TEST_AdvertItems"
    )

    search_app.meilisearch_utils.initialise_meilisearch()
