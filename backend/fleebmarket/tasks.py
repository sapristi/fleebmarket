import logging

from django.conf import settings
from fleebmarket.utils import alerts, monitor
from huey import crontab
from huey.contrib.djhuey import periodic_task

logger = logging.getLogger(__name__)


@periodic_task(crontab(minute="00"))
def send_alerts():
    alerts.send(
        discord_token=settings.DISCORD_CREDS["bot_token"],
        since_hours=1,
        test_channel=False,
    )


@periodic_task(crontab(minute="00"))
def save_monitor_metrics():
    monitor.put_to_disk()
