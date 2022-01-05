from utils import ModelForm
from django import forms
from .models import FirstSurveyData


class FirstSurveyForm(ModelForm):
    class Meta:
        model = FirstSurveyData
        fields = '__all__'
        labels = {
            'trade_frequency': ('How often do you trade keyboard related items ?'),
            'most_used_service': ('Which second hand keyboard market service do you use ?'),
            'service_interest': ('Would you be interested in using a dedicated service ?'),
            'essential_features': ('What are the essential features of the service you actually use ?'),
            'missed_features': ('What features do you miss the most in the service you use ?'),
            'would_pay': ('Would you be ready to pay a small monthly fee (between 1 and 2€) for some advanced features  ?'),
            'paying_features': ('If yes, what kind of feature ?'),
            'how_many_keebs': ('How many keyboards do you own ?'),
            'like_fleebmarket': ('Do you like the name fleebmarket?'),
            'anything_else': ('Anything else you\'d like to tell me ?'),
            'current_year': ("What is the current year ? [CAPTCHA]"),
        }
        widgets = {
            'essential_features': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'missed_features': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'paying_features': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
            'anything_else': forms.Textarea(attrs={'cols': 80, 'rows': 5}),
        }
