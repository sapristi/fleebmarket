from django.conf import settings
from django.db import models
from search_app.models import RedditAdvert, RedditAdvertType
from utils import ChoiceEnum


class AlertAdType(str, ChoiceEnum):
    Selling = RedditAdvertType.Selling.value
    Buying = RedditAdvertType.Buying.value
    Trading = RedditAdvertType.Trading.value
    Giveaway = RedditAdvertType.Giveaway.value
    Group_buy = RedditAdvertType.Group_buy.value
    Any = RedditAdvertType.Any.value


class Region(str, ChoiceEnum):
    EU = "EU"
    US = "US"
    CA = "CA"
    OTHER = "OTHER"
    Any = "Any"


# Create your models here.
class Alert(models.Model):
    terms = models.CharField(max_length=200)
    sensitivity = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    ad_type = models.CharField(max_length=30, choices=AlertAdType.choices())
    region = models.CharField(max_length=30, choices=Region.choices())
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


class AlertMatch(models.Model):
    alert_id = models.ForeignKey(Alert, on_delete=models.CASCADE)
    advert_id = models.ForeignKey(RedditAdvert, on_delete=models.CASCADE)
