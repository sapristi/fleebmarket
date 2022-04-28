from django.urls import path

from . import views

app_name = "survey"
urlpatterns = [path("", views.TakeFirstSurvey.as_view(), name="take")]
