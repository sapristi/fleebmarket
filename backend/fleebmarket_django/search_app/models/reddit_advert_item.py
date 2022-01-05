import logging
from django.db import models
from django.db.models.fields.json import JSONField
from django.utils.html import strip_tags

from search_app.meilisearch_utils import MAdvertsItemsIndex

from .reddit_advert import RedditAdvert

logger = logging.getLogger(__name__)


class RedditAdvertItem(models.Model):
    id = models.AutoField(primary_key=True)
    reddit_advert = models.ForeignKey(RedditAdvert, on_delete=models.CASCADE)
    price = models.IntegerField()
    sold = models.BooleanField()
    full_text = models.TextField(blank=True)
    extra = JSONField(blank=True, null=True)

    def serialize_meilisearch(self):
        res = {
            "pkey": self.id,
            "source": "/r/mechmarket",
            "price": self.price,
            "sold": self.sold,
            "reddit_id": self.reddit_advert.reddit_id,
            "ad_type": self.reddit_advert.ad_type,
            "region": self.reddit_advert.region,
            "created_utc": self.reddit_advert.created_utc.timestamp(),
            "text": strip_tags(self.full_text),
        }
        for k, v in self.extra.items():
            if isinstance(v, str):
                res[k] = v
        return res

    def delete(self, *args, **kwargs):
        MAdvertsItemsIndex.add_to_delete(self.id)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        MAdvertsItemsIndex.add_to_add(
            self.serialize_meilisearch()
        )

