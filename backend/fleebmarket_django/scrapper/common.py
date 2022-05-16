import logging
from datetime import datetime
from typing import Optional

import praw
from dateutil import tz
from django.conf import settings
from praw.models import Submission as PrawSubmission
from pydantic import BaseModel
from search_app.models import RedditAdvert, RedditAdvertType, reddit_advert

logger = logging.getLogger(__name__)
REDDIT_CLIENT = praw.Reddit(
    **settings.SCRAPPER["REDDIT_APP"], user_agent="parse /r/mechmarket"
)


class ParsedSubmission(BaseModel):
    reddit_id: str
    title: str
    ad_type: Optional[str]
    created_utc: str
    author: str
    full_text: str

    @staticmethod
    def from_id(reddit_id):
        sub = praw.models.Submission(REDDIT_CLIENT, id=reddit_id)
        return ParsedSubmission.from_praw(sub)

    @staticmethod
    def from_praw(sub):
        # when submission was deleted
        if sub.author is None:
            return None

        created_utc_dt = datetime.utcfromtimestamp(sub.created_utc).replace(
            tzinfo=tz.UTC
        )
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
