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
from search_app.models import RedditAdvert, RedditAdvertItem


@pytest.mark.django_db(transaction=True)
def test_add_advert():
    submissions = [
        PrawSubmissionMock(
            id="test0",
            title=ok_title,
            link_flair_text="Selling",
            created_utc=1619283556,
            selftext=body,
            author=PrawAuthorMock(name="test_author"),
        ),
        PrawSubmissionMock(
            id="test1",
            title=ok_title,
            link_flair_text="Buying",
            created_utc=1619283556,
            selftext=body,
            author=PrawAuthorMock(name="test_author"),
        ),
        PrawSubmissionMock(
            id="test2",
            title=ko_title,
            link_flair_text="Buying",
            created_utc=1619283556,
            selftext=body,
            author=PrawAuthorMock(name="test_author"),
        ),
        PrawSubmissionMock(
            id="test3",
            title=ko_title,
            link_flair_text="BADBAD",
            created_utc=1619283556,
            selftext=body,
            author=PrawAuthorMock(name="test_author"),
        ),
    ]
    add_submissions(submissions)  #  type: ignore

    assert len(RedditAdvert.objects.all().filter(reddit_id="test0")) == 1
    assert len(RedditAdvert.objects.all().filter(reddit_id="test1")) == 1
    assert len(RedditAdvert.objects.all().filter(reddit_id="test2")) == 0
    assert len(RedditAdvert.objects.all().filter(reddit_id="test3")) == 0

    assert len(RedditAdvert.objects.all()) == 2


@pytest.mark.django_db(transaction=True)
def test_add_advert_w_advert_items():
    submissions = [
        PrawSubmissionMock(
            id="test0",
            title=ok_title,
            link_flair_text="Selling",
            created_utc=1619283556,
            selftext=body_simple,
            author=PrawAuthorMock(name="test_author"),
        ),
    ]

    add_submissions(submissions)
    while is_indexing():
        time.sleep(0.1)

    assert len(RedditAdvert.objects.all()) == 1

    doc = MAdvertsIndex.client().get_document("test0")
    assert doc["reddit_id"] == "test0"

    docs = MAdvertsItemsIndex.client().get_documents()["results"]

    assert len(docs) == 2

    assert len(RedditAdvertItem.objects.all()) == 2
