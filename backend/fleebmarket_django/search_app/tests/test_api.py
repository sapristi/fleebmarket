import os
from datetime import datetime, timedelta

import pytest
from accounts.models import CustomUser
from fastapi.testclient import TestClient
from fleebmarket.asgi import app


@pytest.fixture
def db_user():
    user = CustomUser.objects.create_user(
        username="jacob", email="jacob@…", password="top_secret"
    )
    return user


ok_title = "[RU][H] Supa Dupa Pre-Assembled Corne PCBs [W] Paypal"
ko_title = "HEERE[W] Supa Dupa Pre-Assembled Corne PCBs [W] Paypal"

body = """[Timestamp](https://imgur.com/a/lqGir8t)\n\n&#x200B;\n\nSA-P Snow Cap:\n\n\\-Alphas-60% Icon kit-7u Spacebar-R1:Delete (1u)-R3: 2x Windows Icon (1u), 2x Alt Icon (1.5U)-R4: Shift Icon(1.75u)\n\nLoved the sound and feel of this set, used for a few weeks, just decided I prefer KAT to SA so this set sees little use. Cost about $120 for all brand new -  $75\n\n&#x200B;\n\nJelly Key:\n\nThe Rehabilitation of Lost Cities artisan keycaps - Amazil City, SA R3 - 2.25\n\nPurchased this for the SA Set, no use for it now, only mounted once, just looking to get back what I paid - $65"""

client = TestClient(app)


headers = {"token": os.environ["SERVICE_ACCOUNT_TOKEN"]}


@pytest.mark.django_db(transaction=True)
def test_create_mechmarket_advert():

    response = client.post(
        "/api/scrapper/",
        json=[
            {
                "reddit_id": "test0",
                "title": ok_title,
                "ad_type": "Selling",
                "created_utc": "2020-10-20T12:05",
                "full_text": body,
                "author": "test_author",
            },
            {
                "reddit_id": "test1",
                "title": ok_title,
                "ad_type": "Buying",
                "created_utc": 1619283556,
                "created_utc": "2020-10-20T12:01",
                "full_text": body,
                "author": "test_author",
            },
            {
                "reddit_id": "test2",
                "title": ko_title,
                "ad_type": "Buying",
                "created_utc": 1619283556,
                "created_utc": "2020-10-20T12:03",
                "full_text": body,
                "author": "test_author",
            },
            {
                "reddit_id": "test3",
                "title": ko_title,
                "ad_type": "BADBAD",
                "created_utc": 1619283556,
                "created_utc": "2020-10-20T12:03",
                "full_text": body,
                "author": "test_author",
            },
        ],
        headers=headers,
    )
    print("RESP", response.json())
    assert response.json() == {
        "added": ["test0", "test1"],
        "skipped": ["test2", "test3"],
        "failed": [],
    }
    assert response.status_code == 201
    # assert len(meili_mock["Adverts"]) == 2

    response = client.get("/api/search/")
    data = response.json()
    assert len(data) == 2
    assert data[0]["reddit_id"] == "test0"


@pytest.mark.django_db(transaction=True)
def test_update_advert():
    body1 = "body1"
    body2 = "body2"
    client.post(
        "/api/scrapper/",
        json=[
            {
                "reddit_id": "test0",
                "title": ok_title,
                "ad_type": "Selling",
                "created_utc": (datetime.now() - timedelta(days=5)).isoformat(),
                "full_text": body1,
                "author": "test_author",
            }
        ],
        headers=headers,
    )

    response = client.get(
        "/api/scrapper/to_update", params={"min_score": 0}, headers=headers
    )
    data = response.json()
    assert len(data["to_update"]) == 1

    advert_id = data["to_update"][0]["reddit_id"]
    response = client.patch(
        "/api/scrapper/",
        json=[
            {
                "reddit_id": advert_id,
                "ad_type": "Sold",
                "full_text": body2,
            }
        ],
        headers=headers,
    )
    print(response.text)
    assert response.status_code == 200

    response = client.get("/api/search/")
    data = response.json()
    assert len(data) == 1
    assert data[0]["ad_type"] == "Sold"
    assert data[0]["full_text"] == "body2"


@pytest.mark.django_db(transaction=True)
def test_delete_advert():
    response = client.post(
        "/api/scrapper/",
        json=[
            {
                "reddit_id": "test0",
                "title": ok_title,
                "ad_type": "Selling",
                "created_utc": "2020-10-20T12:05",
                "full_text": body,
                "author": "test_author",
            }
        ],
        headers=headers,
    )
    response = client.delete("/api/scrapper/", json=["test0"], headers=headers)
    response.raise_for_status()
    response = client.get("/api/search/")
    assert len(response.json()) == 0
