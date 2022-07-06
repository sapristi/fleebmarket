import time

import pytest
from scrapper.fetch_new_adverts import add_submissions
from scrapper.tests.common import (
    PrawAuthorMock,
    PrawSubmissionMock,
    body,
    body_simple,
    body_simple_sold_keyboard,
    ko_title,
    ok_title,
)
from search_app.meilisearch_utils import MAdvertsIndex, MAdvertsItemsIndex, is_indexing
from search_app.models.common import RedditAdvertType
from search_app.views.search import search_wrapped

advert_body = """
|desc|price|
|:-|:-|
|cherry|$50|
|boba|$6|
"""


@pytest.mark.django_db(transaction=True)
def test_search_advert():
    submissions = [
        PrawSubmissionMock(
            id="test0",
            title=ok_title,
            link_flair_text="Selling",
            created_utc=1619283556,
            selftext=advert_body,
            author=PrawAuthorMock(name="test_author"),
        ),
    ]

    add_submissions(submissions)  #  type: ignore
    while is_indexing():
        time.sleep(0.1)

    docs = search_wrapped(
        terms="boba", type=RedditAdvertType.Selling, region=None, limit=10, offset=0
    )
    assert len(docs) == 1
