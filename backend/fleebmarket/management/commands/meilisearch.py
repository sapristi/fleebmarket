import djclick
from fleebmarket.utils.misc import ManagementLogging

ml = ManagementLogging()

from search_app.meilisearch_utils import (
    MAdvertsIndex,
    MAdvertsItemsIndex,
    clear_meilisearch,
    initialise_meilisearch,
)
from search_app.models import RedditAdvert, RedditAdvertItem

logger = ml.getLogger()


@djclick.command()
@djclick.pass_verbosity
@djclick.option(
    "-a",
    "--action",
    type=djclick.Choice(["setup", "populate"]),
    required=True,
    help="Select action to perform",
)
@djclick.option("--clear/--no-clear", default=False)
def handle(clear, action, verbosity):
    """Manage meiliserch indices"""
    ml.set_level_from_verbosity(verbosity)
    if clear:
        clear_meilisearch()
    if action == "setup":
        initialise_meilisearch()

    if action == "populate":
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
