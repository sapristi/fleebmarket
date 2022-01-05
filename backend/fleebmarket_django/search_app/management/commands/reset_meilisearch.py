from more_itertools import chunked
import logging

from search_app.models import RedditAdvert
from django.core.management.base import BaseCommand
from ...meilisearch_utils import clear_meilisearch, initialise_meilisearch, meili_client

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--clear-meili', action="store_true")
        parser.add_argument('--populate-from-db', action="store_true")

    def handle(self, clear_meili, populate_from_db, *args, **kwargs):
        if clear_meili:
            clear_meilisearch()
        initialise_meilisearch()

        if populate_from_db:
            adverts = RedditAdvert.objects.all()
            logger.info("Found %s adverts in db", len(adverts))
            chunks = chunked(adverts, 100)
            for chunk in chunks:
                for ad in chunk:
                    ad.update_extra()
                to_update = [ad.serialize_meilisearch() for ad in chunk]
                meili_client.index("Adverts").update_documents(to_update)
            logger.info("Adverts fed to meilisearch")
