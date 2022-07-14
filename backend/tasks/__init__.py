import os
from functools import wraps

import fleebmarket.runtime_setup
from uwsgi_tasks import cron, django_setup

django_setup()

from django.conf import settings
from django.core.management import call_command
from fleebmarket.utils import alerts, monitor
from scrapper.fetch_new_adverts import fetch_new_adverts
from scrapper.update_adverts import update_job


def are_cronjobs_enabled():
    main_name = os.readlink(f"/etc/nginx/conf-bg/main")
    self_name = os.environ.get("INSTANCE_NAME")
    return main_name == self_name or os.environ.get("CRONJOBS", "").lower() == "true"


def cronjobs_enabled(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not are_cronjobs_enabled():
            return
        return f(*args, **kwargs)

    return wrapper


@cron(minute=0, target="spooler")
@cronjobs_enabled
def send_alerts_cron(_signal_number):
    alerts.send(
        discord_token=settings.DISCORD_CREDS["bot_token"],
        since_hours=1,
        test_channel=False,
    )


@cron(minute=0, target="spooler")
@cronjobs_enabled
def backup(_signal_number):
    call_command("dbbackup", "-z")


@cron(minute=0, target="spooler")
@cronjobs_enabled
def save_metrics_cron(_signal_number):
    monitor.put_to_disk()


@cron(minute=-5, target="spooler")
@cronjobs_enabled
def fetch_adverts_cron(_signal_number):
    fetch_new_adverts(**settings.SCRAPPER["FETCH_NEW_ADVERTS"])


@cron(minute=-5, target="spooler")
@cronjobs_enabled
def update_adverts_cron(_signal_number):
    update_job(update_batch_size=100)
