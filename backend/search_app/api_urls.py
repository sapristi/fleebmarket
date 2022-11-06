from django.urls import path
from search_app.views.search import search
from search_app.views.search_item import search_item

app_name = "search_app_api"
urlpatterns = [
    path("search/", search, name="search"),
    path("search_item/", search_item, name="search_item"),
]
