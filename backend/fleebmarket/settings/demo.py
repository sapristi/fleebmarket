import os

from .base import *

ALLOWED_HOSTS += ["fleebmarket.mmill.eu", "localhost"]


SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "fleebmarket",
        "USER": "fleebmarket",
        "PASSWORD": os.environ["FLEEBMARKET_POSTGRES_PASSWORD"],
        "HOST": os.environ.get("POSTGRES_HOST", ""),
        "PORT": "",
    }
}


syslog_identifier = (
    f"{os.environ.get('SYSLOG_NAME', 'Backend')}[{os.environ['INSTANCE_NAME']}]"
)
default_logger_conf = {
    "handlers": ["journald"],
    "level": "INFO",
    "propagate": False,
}

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "{levelname} {asctime} {module} {process:d} {thread:d} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} [{name}] {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "simple",
        },
        "journald": {
            "class": "cysystemd.journal.JournaldLogHandler",
            "identifier": syslog_identifier,
        },
    },
    "root": {
        "handlers": ["journald"],
        "level": "INFO",
    },
    "loggers": {
        #     'django': default_logger_conf,
        #     'django.template': default_logger_conf,
        #     'search_app': default_logger_conf,
        #     'accounts': default_logger_conf,
        #     'market': default_logger_conf,
        #     'fleebmarket': default_logger_conf,
        #     'uvicorn': default_logger_conf,
    },
}

DEBUG = os.environ.get("DEBUG", "").lower() == "true"
