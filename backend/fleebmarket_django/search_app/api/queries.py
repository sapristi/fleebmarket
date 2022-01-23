import os
from search_app import models
from django.utils import timezone
from datetime import timedelta

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


def get_adverts_to_update(nb, min_score):
    max_update_age = os.environ.get("MAX_UPDATE_AGE", "1 month")
    rows = []
    # adverts with low score
    rows.extend(models.RedditAdvert.objects.raw(
        QUERY_adverts_by_score,
        [max_update_age, min_score, nb]
    ))

    return rows

def get_adverts_without_ad_type():
    return models.RedditAdvert.objects.all().filter(
        ad_type=None, created_utc__gte= timezone.now() - timedelta(hours=2)
    )
