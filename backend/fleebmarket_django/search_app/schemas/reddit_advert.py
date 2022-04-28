import logging
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel
from search_app.models import RedditAdvertType

logger = logging.getLogger(__name__)


class RedditAdvertBase(BaseModel):
    reddit_id: str
    title: str
    ad_type: Optional[RedditAdvertType]
    created_utc: datetime
    full_text: str
    author: str

    def __str__(self):
        return f"[{self.reddit_id}] ({self.full_text})"


class RedditAdvertCreate(RedditAdvertBase):
    pass


class RedditAdvertUpdate(BaseModel):
    reddit_id: str
    ad_type: Optional[RedditAdvertType]
    full_text: str


class RedditAdvertDBBase(RedditAdvertBase):
    id: int
    reddit_id: str
    title: str
    ad_type: Optional[RedditAdvertType]
    created_utc: datetime
    full_text: str
    author: str

    class Config:
        orm_mode = True


class RedditAdvertDBLight(RedditAdvertDBBase):
    pass


class RedditAdvertDB(RedditAdvertDBBase):
    type: str = "advert"
    last_updated: datetime
    extra: dict[str, Any]

    def serialize_meilisearch(self):
        if self.extra is None:
            return None
        res = {
            "source": "/r/mechmarket",
            "reddit_id": self.reddit_id,
            "ad_type": self.ad_type,
            "created_utc": self.created_utc.timestamp(),
        }
        for k, v in self.extra.items():
            if isinstance(v, str):
                res[k] = v
        return res
