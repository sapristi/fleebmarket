import time
from datetime import datetime, timedelta

import djclick
from fleebmarket.utils.misc import ManagementLogging
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm

ml = ManagementLogging()

from search_app.meilisearch_utils import (
    MAdvertsItemsIndex,
    flush_all,
    get_unfinished_tasks,
)
from search_app.models import RedditAdvert, RedditAdvertItem
from search_app.models.reddit_advert import TypesToMeilisearch

logger = ml.getLogger()


@djclick.command()
@djclick.pass_verbosity
@djclick.option(
    "--since-days", type=int, required=False, help="Create and setup indices."
)
@djclick.option(
    "--parse-all",
    is_flag=True,
    help="Parse all adverts, not only those of the right type.",
)
@djclick.option(
    "--reset-indices",
    is_flag=True,
    default=True,
    help="Clear postgres and meiliserch indices for advert items.",
)
def handle(verbosity, since_days: int, parse_all: bool, reset_indices: bool):
    if reset_indices:
        print("Reseting indices")
        MAdvertsItemsIndex.client().delete()
        RedditAdvertItem.objects.all().delete()
        MAdvertsItemsIndex.initialize()
    ml.set_level_from_verbosity(verbosity)
    with logging_redirect_tqdm(loggers=[ml.getLogger()]):

        adverts = RedditAdvert.objects.filter(deleted=False, is_duplicate=False)
        if since_days:
            since = datetime.now() - timedelta(days=since_days)
            adverts = adverts.filter(created_utc__gt=since)
        if not parse_all:
            adverts = adverts.filter(ad_type__in=TypesToMeilisearch)
        logger.info("Found %s adverts in db", len(adverts))
        for advert in tqdm(adverts):
            advert.save()
    logger.info("Adverts parsed anew")
    flush_all()

    print("Waiting for meilisearch to finish indexing...")
    current_meili_tasks = len(get_unfinished_tasks())
    pbar = tqdm(total=current_meili_tasks)
    while True:
        new_current_meili_tasks = len(get_unfinished_tasks())
        pbar.update(current_meili_tasks - new_current_meili_tasks)
        current_meili_tasks = new_current_meili_tasks
        if current_meili_tasks == 0:
            break
        time.sleep(0.2)
