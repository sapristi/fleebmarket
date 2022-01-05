from django.shortcuts import render
from .models import FirstSurveyData
from .forms import FirstSurveyForm
from django.views.generic.edit import CreateView, DeleteView, UpdateView


class TakeFirstSurvey(CreateView):
    model = FirstSurveyData
    success_url = '/'
    template_name = "survey/first_survey.html"
    form_class = FirstSurveyForm
