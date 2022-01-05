from django.urls import path, include
from django.shortcuts import render

def index(request):
    return render(request, 'search_app/index.html')

app_name = "search_app"
urlpatterns = [
    path('', index, name="index"),
]
