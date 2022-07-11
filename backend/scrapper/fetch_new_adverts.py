import logging
from typing import List, Optional

from alerts.actions import send_alerts
from praw.models import Submission
from scrapper.common import REDDIT_CLIENT
from scrapper.parse import parse_submission
from search_app import models
from search_app.meilisearch_utils import flush_all
from search_app.models import RedditAdvert

logger = logging.getLogger(__name__)


def get_last_reddit_id_from_db():
    """Returns the reddit id of the most recent stored /r/mechmarket advert"""
    last_id_set = (
        models.RedditAdvert.objects.order_by("-created_utc")
        .values("reddit_id")
        .all()[:1]
    )
    if len(last_id_set) > 0:
        return last_id_set[0]["reddit_id"]
    else:
        return None


def get_last_valid_reddit_id():
    """Get last reddit_id, and checks that the associated post is still valid.
    If the post is no longer valid, delete it from the db, and start again.
    """
    last_reddit_id_db = get_last_reddit_id_from_db()
    if last_reddit_id_db is None:
        return None

    sub = Submission(REDDIT_CLIENT, id=last_reddit_id_db)
    reddit_advert = parse_submission(sub)
    if reddit_advert is None:
        models.RedditAdvert.objects.get(reddit_id=last_reddit_id_db).delete()
        return get_last_valid_reddit_id()
    else:
        return last_reddit_id_db


def get_latest_submissions(
    subreddit: str,
    until_id: Optional[str] = None,
    post_limit: int = 1000,
):
    """Fetches the latest posts from the given subreddit.
    If until_id is provided, do not return the posts following it.
    """
    submissions: List[Submission] = REDDIT_CLIENT.subreddit(subreddit).new(
        limit=post_limit
    )
    res = []
    for sub in submissions:
        if until_id is not None and sub.id == until_id:
            logger.info("Stopping at id %s", until_id)
            break
        res.append(sub)
    else:
        if until_id is not None:
            logger.warning(
                "Could not find %s in last %s new posts", until_id, post_limit
            )

    logger.info("Found %s new submissions in %s", len(res), subreddit)
    return sorted(res, key=lambda sub: sub.created_utc)


def add_submissions(submissions: list[Submission]):
    added_adverts = []

    for submission in submissions:
        if submission is None:
            continue
        reddit_advert = parse_submission(submission)
        if reddit_advert is None:
            continue
        if RedditAdvert.objects.filter(reddit_id=reddit_advert.reddit_id).exists():
            logger.warning(
                "Advert with reddit_id %s already exists; skipping",
                reddit_advert.reddit_id,
            )
            continue

        try:
            reddit_advert.save()
        except Exception as exc:
            logger.warning("Failed saving advert %s", reddit_advert)
            logger.warning(exc, exc_info=True)
            continue

        reddit_advert.mark_duplicates()
        added_adverts.append(reddit_advert)
    logger.info("Saved %s adverts.", len(added_adverts))
    flush_all()
    if len(added_adverts) > 0:
        send_alerts(added_adverts)


def fetch_new_adverts(subreddit: str, post_limit: int = 1000):
    """Fetch new adverts from reddit, and add them to the db."""
    last_valid_reddit_id = get_last_valid_reddit_id()
    logger.info("Last advert id is [%s]", last_valid_reddit_id)
    submissions = get_latest_submissions(subreddit, last_valid_reddit_id, post_limit)
    add_submissions(submissions)
