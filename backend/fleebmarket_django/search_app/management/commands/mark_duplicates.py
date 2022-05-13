import logging

import djclick
from django.db import connection
from tqdm import tqdm
from tqdm.contrib.logging import logging_redirect_tqdm
from utils import ManagementLogging

ml = ManagementLogging()

from search_app.meilisearch_utils import flush_all
from search_app.models import RedditAdvert, RedditAdvertType

logger = ml.getLogger()


@djclick.command()
@djclick.pass_verbosity
@djclick.option(
    "--reset-duplicates",
    help="Set all duplicate status to False before applying",
    is_flag=True,
)
@djclick.option("--wait", is_flag=True, help="User input at each step")
def handle(reset_duplicates, wait, verbosity):
    logging.info(
        f"Before: duplicates: %d, not duplicates: %d",
        RedditAdvert.objects.filter(is_duplicate=True).count(),
        RedditAdvert.objects.filter(is_duplicate=False).count(),
    )
    ml.set_level_from_verbosity(verbosity)
    if reset_duplicates:
        with connection.cursor() as cursor:
            logger.info("Resetting all duplicate status")
            cursor.execute(
                f"UPDATE {RedditAdvert._meta.db_table} set is_duplicate = false"
            )
    to_treat = RedditAdvert.objects.filter(
        ad_type__in=(RedditAdvertType.Selling, RedditAdvertType.Buying),
    )
    with logging_redirect_tqdm():
        for advert in tqdm(to_treat):
            advert.mark_duplicates()
            if wait:
                input()

    flush_all()
    logging.info(
        f"After: duplicates: %d, not duplicates: %d",
        RedditAdvert.objects.filter(is_duplicate=True).count(),
        RedditAdvert.objects.filter(is_duplicate=False).count(),
    )
