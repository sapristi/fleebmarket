import os

from .base import *

if "django.middleware.security.SecurityMiddleware" in MIDDLEWARE:
    index = MIDDLEWARE.index("django.middleware.security.SecurityMiddleware")
else:
    index = 0
# MIDDLEWARE.insert(index + 1, "whitenoise.middleware.WhiteNoiseMiddleware")


ALLOWED_HOSTS += ["*"]
INSTALLED_APPS += []

DEBUG = True


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "fleebmarket",
        "USER": "postgres",
        "PASSWORD": os.environ["POSTGRES_PWD"],
        "HOST": "127.0.0.1",
        "PORT": "5432",
    }
}


CORS_ALLOW_ALL_ORIGINS = True
