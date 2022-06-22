import logging
import os
import pathlib
from typing import Iterable

import meilisearch
from django.conf import settings
from pydantic import BaseModel
from pydantic.fields import Field

logger = logging.getLogger(__name__)

current_dir = pathlib.Path(__file__).parent.absolute()
with open(current_dir / "stopwords") as f:
    stop_words = f.readlines()

meilisearch_host = os.environ["MEILISEARCH_HOST"]
meili_client = meilisearch.Client(meilisearch_host, timeout=5)

ranking_default = [
    "exactness",
    "typo",
    "attribute",
    "proximity",
    "words",
    "created_utc:desc",
]


class MeiliIndexSettings(BaseModel):
    searchableAttributes: list[str]
    # displayedAttributes: list[str] = []
    stopWords: list[str] = stop_words
    rankingRules: list[str] = ranking_default


class MeiliIndex(BaseModel):
    name: str
    settings: MeiliIndexSettings
    pkey: str
    filterableAttributes: list[str]

    # do not initialize those fields; they are used by the instances
    to_add: list[dict] = Field(default_factory=list)
    to_update: list[dict] = Field(default_factory=list)
    to_delete: list[str] = Field(default_factory=list)

    def client(self):
        return meili_client.index(self.name)

    def initialize(self):
        existing_indexes = meili_client.get_indexes()
        existing_index_names = [index.uid for index in existing_indexes]
        if not self.name in existing_index_names:
            logger.info(f"Creating index {self.name}")
            meili_client.create_index(self.name, {"primaryKey": self.pkey})
        else:
            logger.info(f"Index {self.name} already exists")

        # if not self.pkey in self.settings.displayedAttributes:
        #     self.settings.displayedAttributes.append(self.pkey)

        self.client().update_settings(self.settings.dict())
        self.client().update_filterable_attributes(self.filterableAttributes)

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
    settings=MeiliIndexSettings(
        searchableAttributes=["offers", "wants", "text", "country", "region"]
    ),
    pkey="reddit_id",
    filterableAttributes=["ad_type", "region", "country"],
)
MAdvertsItemsIndex = MeiliIndex(
    name="AdvertItems",
    settings=MeiliIndexSettings(searchableAttributes=["text", "country", "region"]),
    pkey="pkey",
    filterableAttributes=["ad_type", "region", "sold"],
)


def flush_all():
    MAdvertsIndex.flush()
    MAdvertsItemsIndex.flush()


def initialise_meilisearch():
    MAdvertsIndex.initialize()
    MAdvertsItemsIndex.initialize()
    logger.info("Meilisearch initialised")


def clear_meilisearch():
    """Clear indices used."""
    logger.info("Reseting indices")
    indexes = meili_client.get_indexes()
    index_names = [
        index.uid
        for index in indexes
        if index.uid in (MAdvertsIndex.name, MAdvertsItemsIndex.name)
    ]
    logger.info("Deleting indices %s", index_names)
    for index_name in index_names:
        meili_client.index(index_name).delete()


def clear_meilisearch_full():
    """Clear all indices"""
    logger.info("Reseting meilisearch db")

    indexes = meili_client.get_indexes()
    index_names = [index.uid for index in indexes]
    logger.info("Deleting indices %s", index_names)
    for index_name in index_names:
        meili_client.index(index_name).delete()


def is_indexing():
    """Check if meilisearch is indexing"""
    tasks = meili_client.get_tasks()
    return all(task["finishedAt"] is not None for task in tasks["results"])
