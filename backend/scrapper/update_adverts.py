import logging
import os
from datetime import timedelta
from statistics import mean

from django.db.models import Q
from django.utils import timezone
from praw.models import Submission
from scrapper.common import REDDIT_CLIENT
from scrapper.parse import parse_submission
from search_app import models
from search_app.meilisearch_utils import flush_all
from search_app.models import RedditAdvert, RedditAdvertType
from six import unichr

logger = logging.getLogger(__name__)
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


def get_to_refresh(nb: int = 100, min_score: float = 1.0):
    """Return adverts that should be refreshed:
    - adverts with high refresh score, less than 1 month old
    - adverts without flair
    - adverts more than 1 month old, less than 300 days old, once a week
    - recent, deleted adverts (pending approval ?)
    """
    max_update_age = os.environ.get("MAX_UPDATE_AGE", "1 month")
    high_score_ads = models.RedditAdvert.objects.raw(
        QUERY_adverts_by_score, [max_update_age, min_score, nb]
    )
    scores = [item.score for item in high_score_ads]
    if len(scores):
        mean_score = mean(scores)
    else:
        mean_score = None

    without_type = models.RedditAdvert.objects.all().filter(
        ad_type=None, created_utc__gte=timezone.now() - timedelta(hours=2)
    )
    old_adverts = (
        models.RedditAdvert.objects.filter(
            created_utc__lte=timezone.now() - timedelta(days=30),
            created_utc__gte=timezone.now() - timedelta(days=300),
            last_updated__lte=timezone.now() - timedelta(days=7),
        )
        .exclude(ad_type=RedditAdvertType.Sold)
        .exclude(ad_type=RedditAdvertType.Purchased)
    )
    recent_deleted = models.RedditAdvert.objects.filter(
        deleted=True,
        created_utc__gte=timezone.now() - timedelta(days=7),
        last_updated__lte=timezone.now() - timedelta(days=1),
    )

    to_refresh = [*high_score_ads, *without_type, *recent_deleted]
    if len(to_refresh) < 100:
        to_refresh.extend(old_adverts[: 100 - len(to_refresh)])

    logger.info(
        "Got %s adverts to refresh; mean score is %s", len(to_refresh), mean_score
    )
    return to_refresh


def update_adverts(to_refresh: list[RedditAdvert]):

    to_update: list[RedditAdvert] = []
    unchanged: list[RedditAdvert] = []
    to_delete: list[RedditAdvert] = []
    errors: list[str] = []

    for old_advert in to_refresh[::-1]:
        reddit_id = old_advert.reddit_id
        try:
            sub = Submission(REDDIT_CLIENT, id=reddit_id)
            new_advert = parse_submission(sub)

            if new_advert is None:
                to_delete.append(old_advert)
                continue

            if (
                new_advert.ad_type != old_advert.ad_type
                or new_advert.full_text != old_advert.full_text
            ):
                old_advert.ad_type = new_advert.ad_type
                old_advert.full_text = new_advert.full_text
                old_advert.extra = new_advert.extra
                old_advert.deleted = False
                to_update.append(old_advert)

            else:
                unchanged.append(old_advert)

        except Exception as exc:
            logger.exception("Failed fetching advert %s: %s", reddit_id, exc)
            errors.append(reddit_id)

    logger.info(
        "%s adverts to update: %s", len(to_update), [ad.reddit_id for ad in to_update]
    )
    logger.info("%s adverts unchanged", len(unchanged))
    logger.info(
        "%s adverts to delete: %s", len(to_delete), [ad.reddit_id for ad in to_delete]
    )
    if len(errors) > 0:
        logger.info("%s adverts in error%s ", len(errors))

    for old_advert in to_delete:
        old_advert.deleted = True
        old_advert.last_updated = timezone.now()
    RedditAdvert.objects.bulk_update(to_delete, ["last_updated"])

    for old_advert in unchanged:
        old_advert.last_updated = timezone.now()
    RedditAdvert.objects.bulk_update(unchanged, ["last_updated"])

    for old_advert in to_update:
        old_advert.last_updated = timezone.now()
        old_advert.save()

    flush_all()


def update_job(update_batch_size, min_score=1.0):
    to_refresh = get_to_refresh(update_batch_size, min_score)
    update_adverts(to_refresh)
