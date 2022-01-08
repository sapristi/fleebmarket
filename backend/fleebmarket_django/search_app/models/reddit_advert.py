import logging
from django.db import models
from django.db.models.fields.json import JSONField

from advert_parsing import parse

from search_app.meilisearch_utils import MAdvertsIndex

from .common import RedditAdvertType
from .parse import parse_mechmarket_advert

logger = logging.getLogger(__name__)


class RedditAdvert(models.Model):
    reddit_id = models.CharField(max_length=20, unique=True, db_index=True)
    title = models.CharField(max_length=2000)
    ad_type = models.CharField(max_length=20, choices=RedditAdvertType.choices(), db_index=True, blank=True, null=True)
    created_utc = models.DateTimeField(db_index=True)
    full_text = models.TextField(blank=True)
    author = models.CharField(max_length=100)
    last_updated = models.DateTimeField(auto_now=True, db_index=True)
    extra = JSONField(blank=True, null=True)

    def update_extra(self):
        extra = parse_mechmarket_advert(
            self.ad_type, self.title, self.full_text
        )
        self.extra = extra
        try:
            self.save()
        except ValueError as exc:
            from django.forms.models import model_to_dict
            logger.error("Failed saving model: %s; model data is %s", self, model_to_dict(self))
            raise exc from None

    def serialize_meilisearch(self):
        if not self.ad_type in (RedditAdvertType.Selling, RedditAdvertType.Buying, RedditAdvertType.Trading):
            return None
        if self.extra is None:
            return None
        res = {
            "source": "/r/mechmarket",
            "reddit_id": self.reddit_id,
            "ad_type": self.ad_type,
            "created_utc": self.created_utc.timestamp(),
        }
        for key in ["text", "wants", "offers", "region", "country"]:
            if not isinstance(self.extra[key], str):
                print(res)
                raise
            res[key] = self.extra[key]
        return res

    def save_meilisearch(self):
        self_meili = self.serialize_meilisearch()
        if self_meili is not None:
            MAdvertsIndex.add_to_update(self_meili)
        else:
            MAdvertsIndex.add_to_delete(self.reddit_id)

    def save(self, *args, **kwargs):
        self.full_text = self.full_text.replace("\x00", "")
        super(RedditAdvert, self).save(*args, **kwargs)
        self.save_meilisearch()

    def delete(self, *args, **kwargs):
        MAdvertsIndex.add_to_delete(self.reddit_id)
        super().delete(*args, **kwargs)

    @property
    def region(self):
        if self.extra is None:
            return None
        return self.extra.get("region")

    def parse_items(self):
        from .reddit_advert_item import RedditAdvertItem # delayed import to avoid circular import issues
        if not self.ad_type in (RedditAdvertType.Selling, RedditAdvertType.Buying, RedditAdvertType.Trading):
            return
        RedditAdvertItem.objects.filter(reddit_advert=self).delete()
        items = parse(self.full_text)
        for item in items:
            if item.relevant_price == None:
                continue
            item_obj = RedditAdvertItem(
                reddit_advert=self,
                price=item.relevant_price.amount,
                sold=item.sold,
                full_text=item.ast.to_html(),
                extra={}
            )
            item_obj.save()
