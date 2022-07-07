import logging
import pathlib
from enum import Enum
from typing import Annotated, Generic, Type, TypeVar, get_origin, get_type_hints

import meilisearch
from django.conf import settings
from pydantic import BaseModel, Field, PrivateAttr
from pydantic.generics import GenericModel

logger = logging.getLogger(__name__)

current_dir = pathlib.Path(__file__).parent.absolute()
with open(current_dir / "stopwords") as f:
    stop_words = f.readlines()

meilisearch_host = settings.MEILISEARCH["host"]
meili_client = meilisearch.Client(meilisearch_host, timeout=5)

ranking_default = [
    "exactness",
    "typo",
    "attribute",
    "proximity",
    "words",
    "created_utc:desc",
]


class MeiliTypoToleranceSettings(BaseModel):
    disableOnWords: list[str]


class MeiliIndexSettings(BaseModel):
    stopWords: list[str] = stop_words
    rankingRules: list[str] = ranking_default
    typoTolerance: MeiliTypoToleranceSettings


class FieldMeta(Enum):
    PKey = "pkey"
    Searchable = "searchable"
    Filterable = "filterable"
    Sortable = "sortable"


class BaseRow(BaseModel):
    @classmethod
    def _is_field_meta(cls, field_name: str, meta_value: FieldMeta):
        type_hint = get_type_hints(cls, include_extras=True)[field_name]
        if get_origin(type_hint) is not Annotated:
            return False
        return meta_value in type_hint.__metadata__

    @classmethod
    def _get_fields_meta(cls, meta_value: FieldMeta) -> list[str]:
        field_names = cls.__fields__.keys()
        return [name for name in field_names if cls._is_field_meta(name, meta_value)]

    @classmethod
    def _pkey(cls):
        pkeys = cls._get_fields_meta(FieldMeta.PKey)
        if len(pkeys) != 1:
            raise ValueError(f"Primary keys: got {pkeys}, expecting single value.")
        return pkeys[0]

    @classmethod
    def _settings(cls):
        return {
            "searchableAttributes": cls._get_fields_meta(FieldMeta.Searchable),
            "filterableAttributes": cls._get_fields_meta(FieldMeta.Filterable),
            "sortableAttributes": cls._get_fields_meta(FieldMeta.Sortable),
        }


RowT = TypeVar("RowT", bound=BaseRow)


class MeiliIndex(GenericModel, Generic[RowT]):
    name: str
    settings: MeiliIndexSettings
    row_type: Type[RowT]

    _to_add: list[RowT] = PrivateAttr(default_factory=list)
    _to_update: list[RowT] = PrivateAttr(default_factory=list)
    _to_delete: list[str] = PrivateAttr(default_factory=list)

    def client(self):
        return meili_client.index(self.name)

    def _settings(self):
        return {**self.settings.dict(), **self.row_type._settings()}

    def initialize(self):
        existing_indexes = meili_client.get_indexes()
        existing_index_names = [index.uid for index in existing_indexes]
        if not self.name in existing_index_names:
            logger.info(f"Creating index {self.name}")
            meili_client.create_index(self.name, {"primaryKey": self.row_type._pkey()})
        else:
            logger.info(f"Index {self.name} already exists")

        self.client().update_settings(self._settings())

    def add_to_update(self, document: RowT):
        self._to_update.append(document)

    def add_to_add(self, document: RowT):
        self._to_add.append(document)

    def add_to_delete(self, doc_id):
        self._to_delete.append(doc_id)

    def flush(self):
        if len(self._to_add) > 0:
            self.client().add_documents([doc.dict() for doc in self._to_add])
            self._to_add = []
        if len(self._to_update) > 0:
            self.client().update_documents([doc.dict() for doc in self._to_update])
            self._to_update = []
        if len(self._to_delete) > 0:
            self.client().delete_documents(self._to_delete)
            self._to_delete = []


class MAdvert(BaseRow):
    reddit_id: Annotated[str, FieldMeta.PKey]
    offers: Annotated[str, FieldMeta.Searchable]
    wants: Annotated[str, FieldMeta.Searchable]
    text: Annotated[str, FieldMeta.Searchable]
    country: Annotated[str, FieldMeta.Searchable, FieldMeta.Filterable]
    region: Annotated[str, FieldMeta.Searchable, FieldMeta.Filterable]
    ad_type: Annotated[str, FieldMeta.Filterable]
    created_utc: Annotated[int, FieldMeta.Sortable]


MAdvertsIndex = MeiliIndex(
    name="Adverts",
    settings=MeiliIndexSettings(
        typoTolerance=MeiliTypoToleranceSettings(disableOnWords=["black", "blank"]),
    ),
    row_type=MAdvert,
)


class MAdvertItem(BaseRow):
    pkey: Annotated[int, FieldMeta.PKey]
    text: Annotated[str, FieldMeta.Searchable]
    country: Annotated[str, FieldMeta.Searchable, FieldMeta.Filterable]
    region: Annotated[str, FieldMeta.Searchable, FieldMeta.Filterable]
    created_utc: Annotated[int, FieldMeta.Sortable]
    sold: Annotated[bool, FieldMeta.Filterable]
    price: Annotated[int, FieldMeta.Sortable]
    ad_type: Annotated[str, FieldMeta.Filterable]
    reddit_id: str


MAdvertsItemsIndex = MeiliIndex(
    name="AdvertItems",
    settings=MeiliIndexSettings(
        typoTolerance=MeiliTypoToleranceSettings(disableOnWords=["black", "blank"]),
    ),
    row_type=MAdvertItem,
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


def get_unfinished_tasks():
    """Check if meilisearch is indexing"""
    tasks = meili_client.get_tasks()
    return [task for task in tasks["results"] if task["finishedAt"] is None]
