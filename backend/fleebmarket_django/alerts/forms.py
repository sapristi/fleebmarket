from django import forms
from utils import ModelForm

from .models import Alert


class AlertForm(ModelForm):
    sensitivity = forms.IntegerField(
        min_value=0, max_value=100, widget=forms.NumberInput(attrs={"class": "input"})
    )

    class Meta:
        model = Alert
        fields = ["terms", "ad_type", "region", "sensitivity", "user"]
        widgets = {
            "terms": forms.TextInput(attrs={"class": "input"}),
            "ad_type": forms.Select(attrs={"class": "select"}),
            "region": forms.Select(attrs={"class": "select"}),
        }


class TestRelevancyForm(forms.Form):
    terms = forms.CharField(label="Search terms", max_length=200)
    full_text = forms.CharField(label="Text", max_length=20000, widget=forms.Textarea)
