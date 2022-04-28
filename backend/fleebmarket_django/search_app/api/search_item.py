import logging

from fastapi import APIRouter, Depends
from search_app.meilisearch_utils import MAdvertsItemsIndex
from search_app.models.reddit_advert_item import RedditAdvertItem

from ..schemas.reddit_advert_item import RedditAdvertItemResponse
from .deps import close_old_connections

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/search_item", dependencies=[Depends(close_old_connections)])


@router.get("/", response_model=list[RedditAdvertItemResponse])
def search_item(
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
        )
        for item in ads_sorted
    ]
