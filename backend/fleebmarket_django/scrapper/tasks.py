import logging

from django.conf import settings
from huey import crontab
from huey.contrib.djhuey import db_periodic_task, db_task, lock_task

logger = logging.getLogger(__name__)

from .fetch_new_adverts import fetch_new_adverts
from .update_adverts import update_adverts


@db_periodic_task(crontab(minute=settings.SCRAPPER["CRON"]))
@lock_task("fetch_task")
def fetch_task():
    fetch_new_adverts(**settings.SCRAPPER["FETCH_NEW_ADVERTS"])


@db_periodic_task(crontab(minute=settings.SCRAPPER["CRON"]))
@lock_task("update_task")
def update_task():
    update_adverts(update_batch_size=100)
