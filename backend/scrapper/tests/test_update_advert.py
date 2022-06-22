import time
from datetime import datetime, timedelta

import pytest
from scrapper import update_adverts
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
def test_update_advert():
    body1 = "body1"
    body2 = "body2"

    submissions = [
        PrawSubmissionMock(
            id="test0",
            title=ok_title,
            link_flair_text="Selling",
            created_utc=int((datetime.now() - timedelta(days=5)).timestamp()),
            selftext=body1,
            author=PrawAuthorMock(name="test_author"),
        )
    ]
    add_submissions(submissions)

    ad = RedditAdvert.objects.get(reddit_id="test0")
    print("AD", ad.created_utc)
    assert len(RedditAdvert.objects.all().filter(reddit_id="test0")) == 1
    assert len(RedditAdvert.objects.all()) == 1
    # We set min score to 0: the ad was updated just now
    to_refresh = update_adverts.get_to_refresh(min_score=0)
    assert len(to_refresh) == 1


def mock_to_refresh(advert):
    def inner(*_args, **_kwargs):
        return [advert]

    return inner


def mock_submission(submission):
    def inner(*_args, **_kwargs):
        return submission

    return inner


@pytest.mark.django_db(transaction=True)
def test_update_advert_w_advert_items(monkeypatch):

    assert len(RedditAdvertItem.objects.all()) == 0
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

    meili_advert = MAdvertsIndex.client().get_document("test0")
    assert meili_advert["reddit_id"] == "test0"

    meili_advert_items = MAdvertsItemsIndex.client().get_documents()
    assert len(meili_advert_items) == 2

    assert len(RedditAdvertItem.objects.all()) == 2

    to_update = RedditAdvert.objects.get(reddit_id="test0")
    new_submission = PrawSubmissionMock(
        id="test0",
        title=ok_title,
        link_flair_text="Selling",
        created_utc=1619283556,
        selftext=body_simple_sold_keyboard,
        author=PrawAuthorMock(name="test_author"),
    )

    monkeypatch.setattr(update_adverts, "get_to_refresh", mock_to_refresh(to_update))
    monkeypatch.setattr(update_adverts, "Submission", mock_submission(new_submission))

    update_adverts.update_adverts(10)
    while is_indexing():
        time.sleep(0.1)

    new_advert = RedditAdvert.objects.get(reddit_id="test0")
    print("TEXT", new_advert.full_text)

    advert_items = RedditAdvertItem.objects.all()
    assert advert_items[0].sold == True
    assert advert_items[1].sold == False

    meili_advert_items = MAdvertsItemsIndex.client().get_documents()

    assert meili_advert_items[0]["sold"] == True
    assert meili_advert_items[1]["sold"] == False
