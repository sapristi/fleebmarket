"""
WSGI config for fleebmarket project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
from pathlib import Path  # Python 3.6+ only

import fleebmarket.runtime_setup
from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()
