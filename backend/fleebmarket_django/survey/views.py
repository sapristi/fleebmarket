from django.shortcuts import render
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from .forms import FirstSurveyForm
from .models import FirstSurveyData


class TakeFirstSurvey(CreateView):
    model = FirstSurveyData
    success_url = "/"
    template_name = "survey/first_survey.html"
    form_class = FirstSurveyForm
