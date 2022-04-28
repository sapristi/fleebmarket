from datetime import datetime, timedelta

from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from utils import ManagementLogging

ml = ManagementLogging()

from django.core.management.base import BaseCommand
from search_app.meilisearch_utils import flush_all
from search_app.models import RedditAdvert, RedditAdvertType, TypesToItemize

logger = ml.getLogger()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--since-days", type=int, default=10, help="Create and setup indices."
        )

    def handle(self, verbosity, since_days, *args, **kwargs):
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
