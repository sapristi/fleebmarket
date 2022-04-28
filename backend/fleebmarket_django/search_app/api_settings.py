import meilisearch
from pydantic import BaseSettings


class Settings(BaseSettings):
    meilisearch_host: str = "127.0.0.1:7700"
    service_account_token: str


settings = Settings()
