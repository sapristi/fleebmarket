from pathlib import Path
import logging
from typing import Optional

import typer

from .looper import Looper
from .scrapper import ParsedSubmission
from .settings import setup_clients, setup_logs

logger = logging.getLogger("scrapper")
app = typer.Typer(no_args_is_help=True, add_completion=False)


@app.command()
def parse_single(
    submission_id: str,
    dotenv: Path = typer.Option('../.env', exists=True, file_okay=True, dir_okay=False),
):
    fl_client, reddit_client = setup_clients(dotenv)
    submission = ParsedSubmission.from_id(reddit_client, submission_id)
    if submission is None:
        logger.error("Failed to parse submission")
        return
    fl_client.add_adverts([submission.dict()])


@app.command()
def loop(
        dotenv: Path = typer.Option('../.env', exists=True, file_okay=True, dir_okay=False),
        subreddit: str = typer.Option("mechmarket", envvar="SCRAPPER_SUBREDDIT"),
        update_batch_size: int = typer.Option(100),
        journald_logs: Optional[str] = typer.Option(None, help="send logs to journald instead of stdout"),
        max_last_submissions: int = typer.Option(1000),
        debug: bool = typer.Option(False),
):
    setup_logs(logger, debug, journald_logs)
    fl_client, reddit_client = setup_clients(dotenv)
    looper = Looper(
        reddit_client,
        fl_client,
        subreddit,
        update_batch_size,
        max_last_submissions
    )
    looper.loop(debug)


if __name__ == '__main__':
    app()
