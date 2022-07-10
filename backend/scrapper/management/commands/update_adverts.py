import djclick
from fleebmarket.utils.misc import ManagementLogging
from scrapper.update_adverts import update_adverts

ml = ManagementLogging()

logger = ml.getLogger()


@djclick.command()
@djclick.option(
    "-s",
    "--batch-size",
    type=int,
    default=100,
)
@djclick.option(
    "-m",
    "--min-score",
    type=int,
    default=1.0,
)
def handle(batch_size: int, min_score: float):
    """Fetch new adverts"""
    update_adverts(update_batch_size=batch_size, min_score=min_score)
