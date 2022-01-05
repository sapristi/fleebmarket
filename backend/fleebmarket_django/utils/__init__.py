from enum import Enum
from django import forms


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
