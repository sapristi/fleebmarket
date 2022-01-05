from typing import Any, Optional
import logging
from pydantic import BaseModel
from fastapi import APIRouter, Depends, BackgroundTasks
from statistics import mean

from alerts.actions import alert_task
from ..schemas.reddit_advert import RedditAdvertDB, RedditAdvertDBLight, RedditAdvertCreate, RedditAdvertUpdate
from search_app import models
from .queries import get_adverts_to_update, get_adverts_without_ad_type
from .deps import meili_session, service_account, close_old_connections

logger = logging.getLogger(__name__)
router = APIRouter(
    prefix="/scrapper",
    dependencies=[
        Depends(service_account),
        Depends(close_old_connections),
        Depends(meili_session)
    ])



class ToUpdateResonse(BaseModel):
    to_update: list[RedditAdvertDBLight]
    mean_score: Optional[float]

@router.get("/to_update", response_model=ToUpdateResonse)
def get_to_update(
    nb:int = 100,
    min_score: float = 1.0
):
    to_update = get_adverts_to_update(nb, min_score)
    scores = [item.score for item in to_update]
    if len(scores):
        mean_score = mean(scores)
    else:
        mean_score = None

    without_type = get_adverts_without_ad_type()

    to_update = [*to_update, *without_type]
    return {"to_update": to_update, "mean_score": mean_score}


@router.get("/last_reddit_id", response_model=Optional[str])
def get_last_reddit_id():
    """Returns the reddit id of the most recent stored /r/mechmarket advert"""
    last_id_set = models.RedditAdvert.objects.order_by('-created_utc').values("reddit_id").all()[:1]
    if len(last_id_set) > 0:
        last_id = last_id_set[0]["reddit_id"]
    else:
        last_id = None
    return last_id

@router.get("/", response_model=list[RedditAdvertDB])
def get_list(offset: int = 0, limit: int = 10):
    objs = models.RedditAdvert.objects.all()[offset:limit]
    return list(objs)

@router.get("/{reddit_id}", response_model=RedditAdvertDB)
def get(reddit_id: str):
    obj = models.RedditAdvert.objects.get(reddit_id=reddit_id)
    return obj

class DeleteResponse(BaseModel):
    deleted: list[str] = []
    failed: list[str] = []

@router.delete("/", response_model=DeleteResponse)
def delete(
    reddit_ids: list[str],
):
    response = DeleteResponse()
    for reddit_id in reddit_ids:
        try:
            models.RedditAdvert.objects.get(reddit_id=reddit_id).delete()
            response.deleted.append(reddit_id)
        except Exception as exc:
            logger.warning(f"Failed deleting advert [{reddit_id}]", exc)
            response.failed.append(reddit_id)
    return response

class CreateResponse(BaseModel):
    added: list[str] = []
    skipped: list[str] = []
    failed: list[str] = []

@router.post("/", status_code=201, response_model=CreateResponse)
def create_batch(
    adverts: list[dict],
    background_tasks: BackgroundTasks,
):
    response = CreateResponse()
    added_adverts = []
    for data_in in adverts:
        try:
            advert_in = RedditAdvertCreate.parse_obj(data_in)
        except Exception as e:
            logger.warning("Could not parse [%s], skipping: %s", data_in.get("reddit_id"), e)
            response.skipped.append(data_in.get("reddit_id", "no_reddit_id"))
            continue

        if (
                advert_in.ad_type is None or
                advert_in.ad_type in models.RedditAdvertType.ignored()
        ):
            continue

        try:
            extra = models.parse_mechmarket_advert(advert_in.ad_type, advert_in.title, advert_in.full_text)
        except Exception as e:
            logger.warning("Could not parse [%s], skipping: %s", data_in.get("reddit_id"), e)
            response.skipped.append(data_in.get("reddit_id", "no_reddit_id"))
            continue

        if extra is None:
            logger.warning(
                "Advert %s will be skipped (%s)",
                advert_in.reddit_id,  advert_in.title
            )
            response.skipped.append(advert_in.reddit_id)
            continue

        advert_db = models.RedditAdvert(
            **advert_in.dict(),
            extra=extra
        )
        try:
            advert_db.save()
        except Exception as exc:
            logger.warning("Failed saving advert %s", advert_db)
            logger.warning(exc, exc_info=True)
            response.failed.append(advert_db.reddit_id)
            continue

        try:
            advert_db.parse_items()
        except Exception as exc:
            logger.error("Failed parsing advert [%s]: %s", advert_in.reddit_id, exc)
            logger.exception(exc)

        response.added.append(advert_in.reddit_id)
        added_adverts.append(advert_db)

    logger.info("Received reddit adverts: %s", response)

    background_tasks.add_task(alert_task, added_adverts)

    return response

@router.patch("/", response_model=None)
def update(
    adverts: list[RedditAdvertUpdate],
):
    updated = []
    to_skip = []
    for advert in adverts:
        if advert.ad_type is None:
            to_skip.append(advert)
            continue
        ad_db : models.RedditAdvert = models.RedditAdvert.objects.get(reddit_id=advert.reddit_id)
        ad_db.ad_type = advert.ad_type
        ad_db.full_text = advert.full_text
        ad_db.update_extra()
        ad_db.parse_items()

        updated.append(advert.reddit_id)

    return None

@router.post("/mark_updated", response_model=None)
def mark_updated(
    advert_ids: list[int]
):
    for advert_id in advert_ids:
        ad_db = models.RedditAdvert.objects.get(pk=advert_id)
        ad_db.save()
    return None
