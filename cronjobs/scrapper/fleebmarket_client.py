import requests
import logging
from urllib.parse import urljoin

logger = logging.getLogger(__name__)

class FLClient():
    def __init__(self, host, token):
        self.session = requests.Session()
        self.session.headers["Token"] = token
        self.host =host

    def get_to_update(self, nb):
        response = self.session.get(
            urljoin(self.host, "/api/scrapper/to_update"),
            params={
                "nb": nb
            }
        )
        response.raise_for_status()
        return response.json()

    def get_last_reddit_id(self):
        response = self.session.get(
            urljoin(self.host, "/api/scrapper/last_reddit_id")
        )
        response.raise_for_status()
        return response.json()

    def add_adverts(self, adverts: list[dict]):
        response = self.session.post(
            urljoin(self.host, "/api/scrapper/"),
            json=adverts
        )
        response.raise_for_status()

    # TODO: handle pagination
    def get_all_adverts(self):
        response = self.session.get(
            urljoin(self.host, "/api/reddit_adverts/")
        )
        response.raise_for_status()
        ads = response.json()
        return ads

    def update_adverts(self, adverts: list[dict]):
        response = self.session.patch(
            urljoin(self.host, "/api/scrapper/"),
            json=adverts
        )
        try:
            response.raise_for_status()
        except Exception as exc:
            logger.error("Batch request failed (%s); retrying in unit mode", exc)
            self.update_adverts_unit(adverts)

    def update_adverts_unit(self, adverts: list[dict]):
        for advert in adverts:
            response = self.session.patch(
                urljoin(self.host, "/api/scrapper/"),
                json=[advert]
            )
            try:
                response.raise_for_status()
            except Exception as exc:
                logger.error("Unit request failed with data: %s", advert)
                logger.error("Exception was: %s", exc)

    def signal_advert_checked(self, advert_ids: list[int]):
        response = self.session.post(
            urljoin(self.host, "/api/scrapper/mark_updated"),
            json=advert_ids
        )
        response.raise_for_status()

    def delete_adverts(self, advert_ids: list[str]):
        response = self.session.delete(
            urljoin(self.host, f"/api/scrapper/"),
            json=advert_ids
        )
        response.raise_for_status()
