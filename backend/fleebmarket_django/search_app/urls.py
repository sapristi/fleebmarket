from django.conf import settings
from django.shortcuts import render
from django.urls import include, path


def index(request):
    context = {
        "react_js": settings.REACT_JS_PATH,
        "react_css": settings.REACT_CSS_PATH,
    }
    return render(request, "search_app/index.html", context)


app_name = "search_app"
urlpatterns = [
    path("", index, name="index"),
]
