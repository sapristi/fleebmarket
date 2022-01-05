import logging
import time
from typing import Optional

from .scrapper import (
    get_last_submissions, treat_submissions,
    update_adverts, ParsedSubmission
)
from .fleebmarket_client import FLClient

logger = logging.getLogger(__name__)

class Looper():
    def __init__(self, reddit_client, fl_client: FLClient, subreddit, update_batch_size, max_last_submissions):
        self.reddit_client = reddit_client
        self.subreddit = subreddit
        self.fl_client = fl_client
        self.update_batch_size = update_batch_size
        self.last_advert_id = None
        self.max_last_submissions = max_last_submissions

    def update(self):
        return update_adverts(self.fl_client, self.reddit_client, self.update_batch_size)

    def get_last_advert_id(self) -> Optional[str]:
        last_id_db = self.fl_client.get_last_reddit_id()
        if last_id_db is None:
            return None
        sub = ParsedSubmission.from_id(self.reddit_client, last_id_db)
        if sub is None or sub.is_deleted():
            self.fl_client.delete_adverts([last_id_db])
            return self.get_last_advert_id()
        return last_id_db

    def fetch_adverts(self):
        last_advert_id = self.get_last_advert_id()
        logger.info("Last advert id is [%s]", last_advert_id)
        submissions = get_last_submissions(self.reddit_client, self.subreddit, last_advert_id, self.max_last_submissions)

        if len(submissions) > 0:
            self.last_advert_id = submissions[-1].id
            treat_submissions(self.fl_client, submissions)

        return len(submissions)

    def loop(self, debug=False):
        while True:
            try:
                nb_event = self.single_loop()
                if nb_event >= 100:
                    tts = 0
                elif nb_event > 50:
                    tts = 30
                elif nb_event > 10:
                    tts = 60
                else:
                    tts = 120
                logger.info("Sleeping for %ss", tts)
                if not debug:
                    time.sleep(tts)
            except Exception as e:
                logger.warning("Loop failed: %s", e)
                logger.exception(e)
                # logger.debug(e, exc_info=True)
                time.sleep(60) 

    def single_loop(self):
        nb_new = self.fetch_adverts()
        nb_updated = self.update()
        return nb_updated + nb_new
