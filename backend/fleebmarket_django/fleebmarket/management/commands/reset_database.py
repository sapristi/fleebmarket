import os

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth import get_user_model


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--clear-migrations', action="store_true")
        parser.add_argument('--force-reset', action="store_true")

    def handle(self, *args, **kwargs):

        call_command("flush", "--noinput")
        call_command("makemigrations")
        call_command("migrate")

        call_command("createsuperuser", username="admin", interactive=False, email="no@no.com")
        User = get_user_model()

        scrapper_pwd = os.environ.get("SCRAPPER_PWD", "scrapper_pwd")
        scrapperUser = User.objects.create_user("scrapper", email="no@no.com", password=scrapper_pwd)
        scrapperUser.save()
        print("scrapper user created")
