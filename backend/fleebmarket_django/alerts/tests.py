from datetime import datetime
from typing import Optional

import pytest
from accounts.models import CustomUser
from pydantic import BaseModel
from search_app.models.common import RedditAdvertType
from search_app.models.reddit_advert import RedditAdvert

from .actions import find_alerts
from .models import Alert, AlertAdType, Region


class AdvertIn(BaseModel):
    reddit_id: str
    title: str
    full_text: str
    ad_type: str
    region: Optional[Region]


@pytest.fixture
def alerts_db():
    user = CustomUser.objects.create_user(
        username="jacob", email="jacob@…", password="top_secret"
    )
    alerts = [
        Alert(
            terms="test1",
            sensitivity=100,
            ad_type=AlertAdType.Any,
            region=Region.Any,
            user=user,
        ),
        Alert(
            terms="test2",
            sensitivity=100,
            ad_type=AlertAdType.Selling,
            region=Region.EU,
            user=user,
        ),
        Alert(
            terms="test3",
            sensitivity=100,
            ad_type=AlertAdType.Buying,
            region=Region.EU,
            user=user,
        ),
    ]
    for alert in alerts:
        alert.save()


@pytest.mark.django_db(transaction=True)
def test_find_alerts(alerts_db, meili_mock):
    advert_0 = RedditAdvert(
        reddit_id="ad1",
        title="title1",
        full_text="test",
        ad_type=RedditAdvertType.Selling,
        extra={"region": Region.EU},
        created_utc=datetime.now(),
    )
    advert_0.save()
    advert_1 = AdvertIn(
        reddit_id="ad2",
        title="title2",
        full_text="test",
        ad_type=RedditAdvertType.Buying,
        region=Region.EU,
    )
    advert_2 = AdvertIn(
        reddit_id="ad3",
        title="title3",
        full_text="test",
        ad_type=RedditAdvertType.Buying,
        region=Region.US,
    )
    advert_3 = AdvertIn(
        reddit_id="ad4",
        title="title4",
        full_text="test",
        ad_type=RedditAdvertType.Buying,
        region=None,
    )

    match_0_raw = list(
        find_alerts([RedditAdvert.objects.get(reddit_id="ad1")]).values()
    )[0]
    match_1_raw = list(find_alerts([advert_1]).values())[0]
    match_2_raw = list(find_alerts([advert_2]).values())[0]
    match_3_raw = list(find_alerts([advert_3]).values())[0]

    match_0 = [alert.terms for (alert, _, _) in match_0_raw]
    match_1 = [alert.terms for (alert, _, _) in match_1_raw]
    match_2 = [alert.terms for (alert, _, _) in match_2_raw]
    match_3 = [alert.terms for (alert, _, _) in match_3_raw]

    assert match_0 == ["test1", "test2"]
    assert match_1 == ["test1", "test3"]
    assert match_2 == ["test1"]
    assert match_3 == ["test1"]
