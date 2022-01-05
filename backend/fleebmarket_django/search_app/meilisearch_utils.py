import logging, pathlib, os
from typing import Iterable
import meilisearch
from django.conf import settings
from pydantic import BaseModel

logger = logging.getLogger(__name__)

current_dir = pathlib.Path(__file__).parent.absolute()
with open(current_dir / "stopwords") as f:
    stop_words = f.readlines()

meilisearch_host = os.environ['MEILISEARCH_HOST']
meili_client = meilisearch.Client(meilisearch_host, timeout=5)

ranking_default = [
  "typo",
  "attribute",
  "proximity",
  "words",
  "wordsPosition",
  "exactness",
  "desc(created_utc)",
]

class MeiliIndexSettings(BaseModel):
    searchableAttributes: list[str]
    displayedAttributes: list[str] = []
    stopWords: list[str] = stop_words
    rankingRules: list[str] = ranking_default

class MeiliIndex(BaseModel):
    name: str
    settings: MeiliIndexSettings
    pkey: str
    faceting_attributes: list[str]

    # do not initialize those fields; they are used by the instances
    to_add: list[dict] = []
    to_update: list[dict] = []
    to_delete: list[dict] = []

    def client(self):
        return meili_client.index(self.name)

    def initialize(self):
        existing_indexes = meili_client.get_indexes()
        existing_index_names = [index["name"] for index in existing_indexes]
        if not self.name in existing_index_names:
            logger.info(f"Creating index {self.name}")
            meili_client.create_index(self.name, {'primaryKey': self.pkey})
        else:
            logger.info(f"Index {self.name} already exists")

        self.client().update_settings(self.settings.dict())
        self.client().update_attributes_for_faceting(self.faceting_attributes)

    def add_to_update(self, document: dict):
        self.to_update.append(document)

    def add_to_add(self, document: dict):
        self.to_add.append(document)

    def add_to_delete(self, doc_id):
        self.to_delete.append(doc_id)

    def flush(self):
        if len(self.to_add) > 0:
            self.client().add_documents(self.to_add)
            self.to_add = []
        if len(self.to_update) > 0:
            self.client().update_documents(self.to_update)
            self.to_update = []
        if len(self.to_delete) > 0:
            self.client().delete_documents(self.to_delete)
            self.to_delete = []

MAdvertsIndex = MeiliIndex(
    name="Adverts",
    settings=MeiliIndexSettings(searchableAttributes=[
        'offers',
        'wants',
        'title_stripped',
        'text',
        'country',
        'region'
    ]),
    pkey="reddit_id",
    faceting_attributes=['ad_type', "region", "country"]
)
MAdvertsItemsIndex = MeiliIndex(
    name="AdvertItems",
    settings=MeiliIndexSettings(searchableAttributes=[
        'text',
        'country',
        'region'
    ]),
    pkey="pkey",
    faceting_attributes=['ad_type', "region", "country"]
)


def initialise_meilisearch():
    MAdvertsIndex.initialize()
    MAdvertsItemsIndex.initialize()
    logger.info("Meilisearch initialised")


def clear_meilisearch():
    logger.info("Reseting meilisearch db")

    indexes = meili_client.get_indexes()
    index_names = [index["name"] for index in indexes]
    for index_name in index_names:
        meili_client.index(index_name).delete()

