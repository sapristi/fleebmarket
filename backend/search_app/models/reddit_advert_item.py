import logging
import re

from django.db import models
from django.db.models.fields.json import JSONField
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from search_app.meilisearch_utils import MAdvertItem, MAdvertsItemsIndex

from .reddit_advert import RedditAdvert

logger = logging.getLogger(__name__)


def custom_strip_tags(value):
    """Returns the given HTML with all tags stripped."""
    return re.sub(r"<[^>]*?>", " ", value)


class RedditAdvertItem(models.Model):
    id = models.AutoField(primary_key=True)
    reddit_advert = models.ForeignKey(RedditAdvert, on_delete=models.CASCADE)
    price = models.IntegerField()
    sold = models.BooleanField()
    full_text = models.TextField(blank=True)
    extra = JSONField(blank=True, null=True)

    def serialize_meilisearch(self):
        return MAdvertItem(
            pkey=self.id,
            price=self.price,
            sold=self.sold,
            reddit_id=self.reddit_advert.reddit_id,
            ad_type=self.reddit_advert.ad_type,
            region=self.reddit_advert.region,
            country=self.reddit_advert.extra.get("country"),
            created_utc=self.reddit_advert.created_utc.timestamp(),
            text=custom_strip_tags(self.full_text),
        )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        MAdvertsItemsIndex.add_to_add(self.serialize_meilisearch())


@receiver(pre_delete, sender=RedditAdvertItem)
def delete_meilisearch(sender, instance, using, **kwargs):
    MAdvertsItemsIndex.add_to_delete(instance.id)
