import pytest
from scrapper.fetch_new_adverts import add_submissions
from scrapper.tests.common import (
    PrawAuthorMock,
    PrawSubmissionMock,
    body,
    ko_title,
    ok_title,
)
from search_app.models import RedditAdvert


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
    add_submissions(submissions)

    assert len(RedditAdvert.objects.all().filter(reddit_id="test0")) == 1
    assert len(RedditAdvert.objects.all().filter(reddit_id="test1")) == 1
    assert len(RedditAdvert.objects.all().filter(reddit_id="test2")) == 0
    assert len(RedditAdvert.objects.all().filter(reddit_id="test3")) == 0

    assert len(RedditAdvert.objects.all()) == 2
