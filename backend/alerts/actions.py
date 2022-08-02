import logging
from collections import defaultdict
from datetime import datetime, timedelta

from django.template.loader import render_to_string
from fuzzywuzzy import fuzz
from search_app.models import RedditAdvert
from uwsgi_tasks import TaskExecutor, task

from .models import Alert, AlertAdType, Region

logger = logging.getLogger(__name__)


def score_advert(terms: list[str], title: str, body: str):
    ratios = [
        max(fuzz.partial_ratio(term, title), fuzz.partial_ratio(term, body))
        for term in terms
    ]
    return sum(ratios) / len(terms)


def find_alerts(adverts: list[RedditAdvert]):
    alerts = Alert.objects.all()
    to_send = defaultdict(list)
    for alert in alerts:
        terms = alert.terms.split()
        for advert in adverts:
            if alert.ad_type != AlertAdType.Any and alert.ad_type != advert.ad_type:
                continue
            if alert.region != Region.Any and alert.region != advert.region:
                # print("BAD region", alert.terms, alert.region, advert.region)
                continue
            # TODO: filter by region
            score = score_advert(terms, advert.title, advert.full_text)
            # print("SCORE", score)
            if score >= alert.sensitivity:
                to_send[alert.user].append((alert, advert, score))

    return to_send


def send_alerts(adverts: list[RedditAdvert], retry_count=5):
    to_send = find_alerts(adverts)
    if len(to_send) > 0:
        send_alerts_spooled(
            [
                (user, render_to_string("alerts/messages/alert", {"data": data}))
                for user, data in to_send.items()
            ]
        )


# TODO: see how we could use https://github.com/Bahus/uwsgi_tasks#task-introspection-api ?
@task(executor=TaskExecutor.SPOOLER, retry_count=2, retry_timeout=300)
def send_alerts_spooled(to_send):
    logger.info("Sending {len(to_send)} alerts.")
    for user, message in to_send:
        user.send_message("Fleebmarket: a post matched one of your alerts", message)

    # sent = 0
    # logger.info(f"{len(to_send)} user alerts to send.")
    # try:
    #     while len(to_send) > 0:
    #         user, message = to_send.pop()
    #         user.send_message("Fleebmarket: a post matched one of your alerts", message)
    #         sent += 1
    # except Exception as exc:
    #     logger.info(
    #         f"Error while sending user alert. {sent} alerts sent; {len(to_send)} still to send ({exc})."
    #     )
    #     retry_at = str(datetime.utcnow() + timedelta(seconds=60))
    #     if retry_counts > 0:
    #         send_alerts_spooled(
    #             to_send=to_send, retry_counts=retry_counts - 1, at=retry_at
    #         )
