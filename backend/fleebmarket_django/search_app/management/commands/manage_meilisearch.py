from utils import ManagementLogging

ml = ManagementLogging()

from django.core.management.base import BaseCommand
from search_app.meilisearch_utils import (
    MAdvertsIndex,
    MAdvertsItemsIndex,
    clear_meilisearch,
    initialise_meilisearch,
)
from search_app.models import RedditAdvert, RedditAdvertItem

logger = ml.getLogger()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument(
            "--clear", action="store_true", help="Clear all data from meilisearch."
        )
        parser.add_argument(
            "--populate-from-db",
            action="store_true",
            help="Inserts data from postgres db into meilisearch.",
        )
        parser.add_argument(
            "--setup-indices", action="store_true", help="Create and setup indices."
        )

    def handle(
        self, clear, populate_from_db, setup_indices, verbosity, *args, **kwargs
    ):
        ml.set_level_from_verbosity(verbosity)
        if clear:
            clear_meilisearch()

        if setup_indices:
            initialise_meilisearch()

        if populate_from_db:
            initialise_meilisearch()
            adverts = RedditAdvert.objects.all()
            logger.info("Found %s adverts in db", len(adverts))
            for ad in adverts:
                ad_meili = ad.serialize_meilisearch()
                if ad_meili is not None:
                    MAdvertsIndex.add_to_add(ad_meili)
            MAdvertsIndex.flush()
            logger.info("Adverts fed to meilisearch")

            advert_items = RedditAdvertItem.objects.all()
            logger.info("Found %s advert_items in db", len(advert_items))
            for ad_item in advert_items:
                ad_item_meili = ad_item.serialize_meilisearch()
                if ad_item_meili is not None:
                    MAdvertsItemsIndex.add_to_add(ad_item_meili)
            MAdvertsItemsIndex.flush()
            logger.info("Adverts fed to meilisearch")
