import djclick
from fleebmarket.utils.misc import ManagementLogging
from scrapper.fetch_new_adverts import fetch_new_adverts

ml = ManagementLogging()

logger = ml.getLogger()


@djclick.command()
@djclick.option(
    "-l",
    "--limit",
    type=int,
    default=100,
)
def handle(limit: int):
    """Fetch new adverts"""
    fetch_new_adverts("mechmarket", post_limit=limit)
