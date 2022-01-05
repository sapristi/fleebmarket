from typing import Optional
from psaw import PushshiftAPI
import praw
import logging
from datetime import datetime
from dateutil import tz
from pydantic import BaseModel

logger = logging.getLogger(__name__)
pushshift = PushshiftAPI()


def sort_submissions(subs):
    res = sorted(subs, key=lambda sub: sub.created_utc)
    if len(res) > 0:
        logger.debug("First %s %s",res[0].id, datetime.utcfromtimestamp(res[0].created_utc))
        logger.debug("Last %s %s", res[-1].id, datetime.utcfromtimestamp(res[-1].created_utc))
    return res


def get_last_submissions(
        reddit_client,
        subreddit: str,
        until_id: str=None,
        n_posts: int = 1000,
):
    """Fetches the last n_posts posts from the given subreddit.
    If until_id is provided, do not return the posts following it.
    """
    submissions = reddit_client.subreddit(subreddit).new(limit=n_posts)
    res = []
    for sub in submissions:
        if until_id is not None and sub.id == until_id:
            logger.info("Stopping at id %s", until_id)
            break
        res.append(sub)
    else:
        if until_id is not None:
            logger.warning("Could not find %s in last %s new posts", until_id, n_posts)

    logger.info("Found %s posts", len(res))
    return sort_submissions(res)


class ParsedSubmission(BaseModel):
    reddit_id: str
    title: str
    ad_type: Optional[str]
    created_utc: str
    author: str
    full_text: str

    @staticmethod
    def from_id(reddit_client, reddit_id):
        sub = praw.models.Submission(reddit_client, id=reddit_id)
        return ParsedSubmission.from_praw(sub)

    @staticmethod
    def from_praw(sub):
        # when submission was deleted
        if sub.author is None:
            return None

        created_utc_dt = datetime.utcfromtimestamp(sub.created_utc).replace(tzinfo=tz.UTC)
        created_utc = created_utc_dt.isoformat()

        if sub.link_flair_text is None:
            logger.warning("Ad without flair: [%s] %s", sub.id, sub.title)

        return ParsedSubmission(
            reddit_id=sub.id,
            title=sub.title,
            ad_type=sub.link_flair_text,
            created_utc=created_utc,
            author=sub.author.name,
            full_text=sub.selftext,
        )

    def is_deleted(self):
        return self.full_text == "[removed]"

    def serialize_update(self: "ParsedSubmission"):
        return self.dict(include={"reddit_id", "ad_type", "full_text"})


def update_adverts(fl_client, reddit_client, update_batch_size):
    to_update_response = fl_client.get_to_update(update_batch_size)
    adverts = to_update_response["to_update"]

    logger.info("Got %s adverts to update; mean score is %s", len(adverts), to_update_response["mean_score"])
    logger.debug(adverts)
    to_update = []
    unchanged = []
    to_delete = []
    for advert in adverts[::-1]:
        reddit_id = advert["reddit_id"]
        try:
            new_advert = ParsedSubmission.from_id(reddit_client, reddit_id)

            if  new_advert is None or new_advert.is_deleted():
                to_delete.append(reddit_id)
                continue

            if (
                    new_advert.ad_type != advert["ad_type"]
                    or new_advert.full_text != advert["full_text"] 
            ):
                to_update.append(new_advert.serialize_update())

            else:
                unchanged.append(advert["id"])

        except Exception as exc:
            logger.warning("Failed fetching advert %s: %s", reddit_id, exc)
            logger.debug(exc, exc_info=True)
            to_delete.append(reddit_id)

    logger.info("%s adverts to update", len(to_update))
    logger.info("%s adverts unchanged", len(unchanged))
    logger.info("%s adverts to delete", len(to_delete))
    logger.info("To delete: %s", to_delete)
    fl_client.update_adverts(to_update)
    fl_client.signal_advert_checked(unchanged)
    fl_client.delete_adverts(to_delete)
    return len(adverts)


def treat_submissions(fl_client, submissions):
    logger.info("Treating %s submissions", len(submissions))
    submissions_all = [ParsedSubmission.from_praw(s) for s in submissions]
    submissions = [s.dict() for s in submissions_all if s is not None and not s.is_deleted()]
    logger.info("Sending %s adverts", len(submissions))
    fl_client.add_adverts(submissions)
