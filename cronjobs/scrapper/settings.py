import logging
from typing import Optional

import coloredlogs
from cysystemd import journal
from pydantic import BaseSettings
import praw
from .fleebmarket_client import FLClient

class Settings(BaseSettings):
    fleebmarket_host: str
    fleebmarket_token: str
    reddit_app_client_id: str
    reddit_app_secret: str

    class Config:
        env_file = '../.env'
        fields = {
            'fleebmarket_token' : {
                'env': 'SERVICE_ACCOUNT_TOKEN'
            }
        }

def setup_clients(dotenv_path):
    settings = Settings(_env_file=dotenv_path)
    fl_client = FLClient(settings.fleebmarket_host, settings.fleebmarket_token)
    reddit_client = praw.Reddit(
        client_id=settings.reddit_app_client_id,
        client_secret=settings.reddit_app_secret,
        user_agent="parse /r/mechmarket"
    )
    return (fl_client, reddit_client)


def setup_logs(logger, debug=False, journald: Optional[str]=None):
    log_level = 'DEBUG' if debug else "INFO"
    if journald:
        logger.setLevel(log_level)
        logger.addHandler(journal.JournaldLogHandler(journald))
        pass
    else:
        handler = logging.StreamHandler()
        logger.addHandler(handler)
        fmt = "%(asctime)s %(name)s:%(lineno)d %(levelname)s %(message)s"
        coloredlogs.install(level=log_level, logger=logger, fmt=fmt)
