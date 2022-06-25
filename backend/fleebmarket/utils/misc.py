import logging
import logging.config
from enum import Enum

from django import forms
from django.conf import settings


class ModelForm(forms.ModelForm):
    required_css_class = "field-required"


class ChoiceEnum(Enum):
    @classmethod
    def choices(cls):
        return ((e.name, e.value) for e in cls.__members__.values())


class ManagementLogging:
    def __init__(self):
        if "journald" in settings.LOGGING["handlers"]:
            settings.LOGGING["handlers"]["journald"]["identifier"] = "DjangoManagement"
        settings.LOGGING["root"]["handlers"].append("console")
        logging.config.dictConfig(settings.LOGGING)

    def getLogger(self):
        return logging.getLogger("Management")

    def set_level_from_verbosity(self, verbosity):
        if verbosity == 0:
            level = logging.WARNING
        elif verbosity == 1:
            level = logging.INFO
        else:
            level = logging.DEBUG

        logging.getLogger().setLevel(level)
        self.getLogger().setLevel(level)
