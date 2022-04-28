from typing import Optional

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from search_app.meilisearch_utils import MAdvertsIndex
from search_app.models import RedditAdvert, RedditAdvertType

from ..schemas.reddit_advert import RedditAdvertDB
from .deps import close_old_connections

router = APIRouter(prefix="/search", dependencies=[Depends(close_old_connections)])


@router.get(
    "/",
    response_model=list[RedditAdvertDB],
    response_model_exclude={"id", "last_updated"},
)
def search(
    terms: str = "",
    type: Optional[RedditAdvertType] = None,
    country: Optional[str] = None,
    region: Optional[str] = None,
    limit: int = 20,
    offset: int = 0,
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
