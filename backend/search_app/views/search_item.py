import logging
from datetime import datetime
from typing import Literal, Optional

from django.http import JsonResponse
from django.http.request import HttpRequest
from pydantic import BaseModel
from search_app.meilisearch_utils import MAdvertsItemsIndex
from search_app.models import RedditAdvertItem, RedditAdvertType

logger = logging.getLogger(__name__)


class SearchItemQuery(BaseModel):
    terms: str = ""
    region: Optional[str] = None
    sold: Literal[""] | Literal["true"] | Literal["false"] = "false"
    limit: int = 20
    offset: int = 0


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
    currency: str


def search_item(request: HttpRequest):
    query = SearchItemQuery.parse_obj(request.GET.dict())
    ads = search_item_wrapped(**query.dict())
    return JsonResponse([ad.dict() for ad in ads], safe=False)


def search_item_wrapped(
    terms: str = "",
    region: str = "",
    sold: str = "",
    limit: int = 20,
    offset: int = 0,
):
    filters = []
    if region:
        filters.append(f"region = {region}")
    if sold:
        filters.append(f"sold = {sold}")

    query_res = MAdvertsItemsIndex.client().search(
        terms,
        {
            "attributesToRetrieve": ["pkey", "sold"],
            "limit": limit,
            "offset": offset,
            "filter": " AND ".join(filters) if filters else None,
        },
    )
    found_ids = [ad["pkey"] for ad in query_res["hits"]]
    ads = RedditAdvertItem.objects.all().filter(id__in=found_ids)
    if len(found_ids) != len(ads):
        missing_ids = set(found_ids) - set(ad.id for ad in ads)
        logger.warning("Missing ads in db: %s", missing_ids)
    ads_sorted = sorted(ads, key=lambda ad: found_ids.index(ad.id))
    return [
        RedditAdvertItemResponse(
            id=item.id,
            reddit_id=item.reddit_advert.reddit_id,
            price=item.price,
            sold=item.sold,
            ad_type=item.reddit_advert.ad_type,
            created_utc=item.reddit_advert.created_utc,
            full_text=item.full_text,
            author=item.reddit_advert.author,
            extra=item.reddit_advert.extra,
            currency=item.extra["currency"],
        )
        for item in ads_sorted
    ]
