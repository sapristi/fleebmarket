from django.core.management.base import BaseCommand, CommandError
from django.core.management import call_command
from django.conf import settings

def setup_dirs():
    print("Creating", settings.DATA_DIR)
    settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Creating", settings.RUNTIME_DATA_DIR)
    settings.RUNTIME_DATA_DIR.mkdir(parents=True, exist_ok=True)
    print("Creating", settings.MEDIA_ROOT)
    settings.MEDIA_ROOT.mkdir(parents=True, exist_ok=True)

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--reset', action="store_true")
        parser.add_argument('--force-reset', action="store_true")
        parser.add_argument('--generate', type=int, default=0)

    def handle(self, *args, **kwargs):

        setup_dirs()

        if kwargs.get("reset"):
            call_command("reset_database")
        elif kwargs.get("force_reset"): 
            call_command("reset_database", force_reset=True)

        nb_to_generate = kwargs.get("generate", 0)
        if nb_to_generate > 0:
            call_command("generate_data", nb=nb_to_generate)
