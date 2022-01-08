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


class AutoEnum(ChoiceEnum):
    @staticmethod
    def _generate_next_value_(name, start, count, last_values):
        return name.replace("_", " ")


class ManagementLogging:
    def __init__(self):
        settings.LOGGING['handlers']['journald']['identifier'] = "DjangoManagement"
        settings.LOGGING['root']['handlers'].append('console')
        logging.config.dictConfig(settings.LOGGING)

    def getLogger(self):
        return logging.getLogger("Management")

    def set_level_from_verbosity(self, verbosity):
        level = logging.INFO if verbosity <= 1 else logging.DEBUG
        logging.getLogger().setLevel(level)
