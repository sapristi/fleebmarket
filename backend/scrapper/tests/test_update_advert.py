from datetime import datetime, timedelta

import pytest
from scrapper.fetch_new_adverts import add_submissions
from scrapper.tests.common import (
    PrawAuthorMock,
    PrawSubmissionMock,
    body,
    ko_title,
    ok_title,
)
from scrapper.update_adverts import get_to_refresh
from search_app.models import RedditAdvert

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
    assert len(RedditAdvert.objects.all()) == 1
    # We set min score to 0: the ad was updated just now
    to_refresh = get_to_refresh(min_score=0)
    assert len(to_refresh) == 1
