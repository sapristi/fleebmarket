from collections import defaultdict
from fuzzywuzzy import fuzz
from django.template.loader import render_to_string

from .models import Alert, AlertAdType, Region
from search_app.models import RedditAdvert

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

def alert_task(adverts: list[RedditAdvert]):
    to_send = find_alerts(adverts)

    for user, data in to_send.items():
        message = render_to_string("alerts/messages/alert", {"data": data})
        user.send_message(
            "Fleebmarket: a post matched one of your alerts",
            message
        )
