"""
ASGI config for fleebmarket project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/asgi/
"""

import os

from django.conf import settings
from django.core.asgi import get_asgi_application

from . import runtime_setup

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fleebmarket.settings")

application = get_asgi_application()


from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from search_app.api import search, search_item

router = APIRouter(prefix="/api")
router.include_router(search.router)
router.include_router(search_item.router)


app = FastAPI(title="fleebmarket", openapi_url=f"/openapi.json")

if settings.DEBUG:
    app.add_middleware(
        CORSMiddleware,
        allow_origins="*",
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(router)
app.mount("/", application)
