import django.db
from fastapi import Header, HTTPException
from ..api_settings import settings
from ..meilisearch_utils import MAdvertsIndex, MAdvertsItemsIndex

def close_old_connections():
    django.db.close_old_connections()


def meili_session():
    yield None
    MAdvertsIndex.flush()
    MAdvertsItemsIndex.flush()

def service_account(token=Header(None)):
    if not token == settings.service_account_token:
        raise HTTPException(status_code=300)

