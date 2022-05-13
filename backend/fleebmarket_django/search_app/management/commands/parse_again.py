from datetime import datetime, timedelta

import djclick
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from utils import ManagementLogging

ml = ManagementLogging()

from search_app.meilisearch_utils import flush_all
from search_app.models import RedditAdvert, TypesToItemize

logger = ml.getLogger()


@djclick.command()
@djclick.pass_verbosity
@djclick.option(
    "--since-days", type=int, required=True, help="Create and setup indices."
)
def handle(verbosity, since_days):
    since = datetime.now() - timedelta(days=since_days)
    ml.set_level_from_verbosity(verbosity)
    with logging_redirect_tqdm(loggers=[ml.getLogger()]):
        adverts = RedditAdvert.objects.filter(
            created_utc__gt=since, ad_type__in=TypesToItemize
        )
        logger.info("Found %s adverts in db", len(adverts))
        for advert in tqdm(adverts):
            advert.parse_items()
    logger.info("Adverts parsed anew")
    flush_all()
