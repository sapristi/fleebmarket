import errno
import logging
import logging.config
import os
import signal
from enum import Enum
from functools import wraps

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


class TimeoutError(Exception):
    pass


def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.setitimer(signal.ITIMER_REAL, seconds)  # used timer instead of alarm
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator
