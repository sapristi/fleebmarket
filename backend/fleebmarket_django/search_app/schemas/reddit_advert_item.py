import logging
from datetime import datetime
from typing import Any, Optional

from pydantic import BaseModel
from search_app.models import RedditAdvertType

logger = logging.getLogger(__name__)


class RedditAdvertItemResponse(BaseModel):
    type: str = "advert_item"
    id: int
    reddit_id: str
    price: int
    sold: bool
    ad_type: Optional[RedditAdvertType]
    created_utc: datetime
    full_text: str
    author: str
    extra: dict

    def __str__(self):
        return f"[{self.reddit_id}] ({self.full_text})"
