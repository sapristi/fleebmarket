import pathlib
import logging

logger = logging.getLogger(__name__)

current_dir = pathlib.Path(__file__).parent.absolute()
with open(current_dir / "stopwords") as f:
    stop_words = f.readlines()

ranking = [
  "typo",
  "attribute",
  "proximity",
  "words",
  "wordsPosition",
  "exactness",
  "desc(created_utc)",
]

WTS_index = {
    'searchableAttributes': [
        'offers',
        'full',
        'country'
    ],
    "displayedAttributes": [],
    "stopWords": stop_words,
    "rankingRules": ranking
}

WTB_index = {
    'searchableAttributes': [
        'wants',
        'full',
        'country'
    ],
    "displayedAttributes": [],
    "stopWords": stop_words,
    "rankingRules": ranking
}

def initialise_meilisearch(meili_client):
    indexes = meili_client.get_indexes()

    index_names = [index["name"] for index in indexes]
    if not "WTS" in index_names:
        logger.info("Creating WTS index")
        meili_client.create_index('WTS', {'primaryKey': 'id'})
    if not "WTB" in index_names:
        logger.info("Creating WTB index")
        meili_client.create_index('WTB', {'primaryKey': 'id'})

    meili_client.index('WTS').update_settings(WTS_index)
    meili_client.index('WTB').update_settings(WTB_index)


def get_last_stored_advert_id(meili_client):
    docs = meili_client.index("WTS").get_documents(
        {"attributesToRetrieve": "id,created_utc"}
    )
    logger.debug("Found %s adverts in meilisearch", len(docs))
    if len(docs) == 0:
        return None
    last_advert = max(docs, key=lambda x: x["created_utc"])
    return last_advert["id"]


def clear_meilisearch(meili_client):
    logger.info("Reseting meilisearch db")

    indexes = meili_client.get_indexes()
    index_names = [index["name"] for index in indexes]
    for index_name in index_names:
        meili_client.index(index_name).delete()
