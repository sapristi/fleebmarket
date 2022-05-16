from datetime import datetime
from typing import Any, Optional

from django.http import JsonResponse
from django.http.request import HttpRequest
from pydantic import BaseModel
from search_app.meilisearch_utils import MAdvertsIndex
from search_app.models import RedditAdvert, RedditAdvertType


class SearchQuery(BaseModel):
    terms: str = ""
    type: Optional[RedditAdvertType] = None
    region: Optional[str] = None
    limit: int = 20
    offset: int = 0


class RedditAdvertResponse(BaseModel):
    id: int
    reddit_id: str
    title: str
    ad_type: Optional[RedditAdvertType]
    created_utc: datetime
    full_text: str
    author: str
    type: str = "advert"
    last_updated: datetime
    extra: dict[str, Any]

    class Config:
        orm_mode = True


def search(request: HttpRequest):
    query = SearchQuery.parse_obj(request.GET.dict())
    ads = search_wrapped(**query.dict())
    return JsonResponse(
        [RedditAdvertResponse.from_orm(ad).dict() for ad in ads], safe=False
    )


def search_wrapped(
    terms: str,
    type: Optional[RedditAdvertType],
    region: Optional[str],
    limit: int,
    offset: int,
):
    filters = []
    if type:
        filters.append(f"ad_type = {type}")

    if region:
        filters.append(f"region = {region}")

    query_res = MAdvertsIndex.client().search(
        terms,
        {
            "attributesToRetrieve": ["reddit_id"],
            "limit": limit,
            "offset": offset,
            "filter": " AND ".join(filters) if filters else None,
        },
    )
    # TODO: since we are filtering the result, the next offset should
    # take this into account
    found_ids = [ad["reddit_id"] for ad in query_res["hits"]]
    ads = RedditAdvert.objects.all().filter(reddit_id__in=found_ids)
    ads_sorted = sorted(ads, key=lambda ad: found_ids.index(ad.reddit_id))
    return ads_sorted
