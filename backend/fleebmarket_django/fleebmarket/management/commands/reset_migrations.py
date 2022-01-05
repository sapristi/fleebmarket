import os
import shutil

from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings
from django.contrib.auth import get_user_model

def get_type(path):
    if path.is_file():
        return "file"
    elif path.is_dir():
        return "dir"
    else:
        return "other"

def remove_dir_content(path, to_exclude=lambda x: False):
    for item in path.iterdir():
        if to_exclude(item):
            print("Not removing", item.name)
            continue
        if item.is_file():
            item.unlink()
        elif item.is_dir():
            shutil.rmtree(item)
        else:
            print(f"I don't know how to remove {item}")

def get_confirmation(text):
    if os.environ.get("FORCE_RESET") == "true":
        return True
    res = input(text +  " y/[n]")
    return res.lower().startswith("y")

def remove_dir(path, to_exclude=lambda x: False):
    try:
        dir_items = [p for p in path.iterdir()]
    except FileNotFoundError:
        print("Not removing file in ", path, ": not found")
        return
    print(f"Directory {path} contains:")
    for item in dir_items:
        print(f" - {item.name} [{get_type(item)}]")
    if get_confirmation("Confirm items deletion ?"):
       remove_dir_content(path, to_exclude)

def remove_file(path):
    if not path.is_file():
        return
    if get_confirmation(f"Remove file {path} ?"):
        path.unlink()


class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('--clear-migrations', action="store_true")
        parser.add_argument('--force-reset', action="store_true")

    def handle(self, force_reset, clear_migrations, *args, **kwargs):

        if force_reset:
            if get_confirmation("RESET WITHOUT CONFIRMATION ?"):
                os.environ["FORCE_RESET"] = "true"

        def exclude_init(elem):
            return elem.name == "__init__.py"

        # remove migrations
        if clear_migrations:
            remove_dir(settings.BASE_DIR / "market" / "migrations", to_exclude=exclude_init)
            remove_dir(settings.BASE_DIR / "cabinet" / "migrations", to_exclude=exclude_init)
            remove_dir(settings.BASE_DIR / "accounts" / "migrations", to_exclude=exclude_init)
            remove_dir(settings.BASE_DIR / "survey" / "migrations", to_exclude=exclude_init)
            remove_dir(settings.BASE_DIR / "search_app" / "migrations", to_exclude=exclude_init)

        call_command("makemigrations")
        call_command("migrate")

        if get_confirmation("Load cities data ?"):
            call_command("cities_light_fixtures", "load")

        call_command("createsuperuser", username="admin", interactive=False, email="no@no.com")
        User = get_user_model()
        scrapper_pwd = os.environ.get("SCRAPPER_PWD")
        if scrapper_pwd is None:
            scrapper_pwd = "scrapper_pwd"
            print("Setting default password password for scrapper:", scrapper_pwd)
        scrapperUser = User.objects.create_user("scrapper", email="no@no.com", password="scrapper_pwd")
        scrapperUser.save()

        if get_confirmation("Clear meilisearch ?"):
            call_command("reset_meilisearch", '--clear-meili')
        else:
            call_command("reset_meilisearch")
