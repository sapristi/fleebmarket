import os
from dataclasses import dataclass
from datetime import datetime, timedelta

import pytest
from accounts.models import CustomUser
from scrapper.fetch_new_adverts import add_submissions
from scrapper.update_adverts import get_to_refresh
from search_app.models import RedditAdvert


@pytest.fixture
def db_user():
    user = CustomUser.objects.create_user(
        username="jacob", email="jacob@…", password="top_secret"
    )
    return user


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


QUERY_adverts_by_score = """
SELECT
    id,
    reddit_id,
    ad_type,
    full_text,
    score
FROM
(
  SELECT
    id,
    stale_h  / greatest(age_d, 1) as score,
    reddit_id,
    ad_type,
    full_text
  FROM
    (
      SELECT
        extract('epoch' from now() - created_utc) / 86400 as age_d,
        extract('epoch' from now() - last_updated) / 3600 as stale_h,
        1 one,
        id,
        reddit_id,
        ad_type,
        full_text
      FROM
        search_app_redditadvert
      WHERE
        ad_type IN ('Selling', 'Buying', 'Trading')
        AND created_utc > now() - INTERVAL %s
        AND is_duplicate = false
    )
    AS T
) as s
where score >= %s
order by score desc
limit %s
"""


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
    # We set min score to 0: the ad was updated just now
    to_refresh = get_to_refresh(min_score=0)
    assert len(to_refresh) == 1
