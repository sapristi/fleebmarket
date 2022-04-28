from collections import defaultdict

import pytest
import search_app.meilisearch_utils


class MeiliIndMock(list):
    def add_documents(self, docs):
        self.extend(docs)

    def update_documents(self, docs):
        self.extend(docs)

    def search(self, *args, **kwargs):
        return {"hits": self}

    def delete_document(self, doc_id):
        doc = [doc for doc in self if doc["reddit_id"] == doc_id]
        if len(doc) == 0:
            raise Exception(f"Doc {doc_id} not found; cannot delete")
        self.remove(doc[0])

    def delete_documents(self, doc_ids):
        for doc_id in doc_ids:
            self.delete_document(doc_id)


class Singleton(type):
    _instances = {}

    def __call__(cls):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__()
        return cls._instances[cls]


class MeiliMock(defaultdict, metaclass=Singleton):
    def __init__(self):
        defaultdict.__init__(self, MeiliIndMock)

    def index(self, ind):
        return self[ind]

    def __repr__(self):
        return str(dict(self))


@pytest.fixture(autouse=True)
def meili_mock(monkeypatch):
    monkeypatch.setattr(search_app.meilisearch_utils, "meili_client", MeiliMock())
