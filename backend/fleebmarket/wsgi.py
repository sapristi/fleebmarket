"""
WSGI config for fleebmarket project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path  # Python 3.6+ only

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fleebmarket.settings")
env_path = Path(__file__).absolute().parent.parent.parent / ".env"
print("Loading .env from", env_path)
load_dotenv(dotenv_path=env_path)

application = get_wsgi_application()
