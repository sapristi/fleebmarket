from django.urls import path

from . import views

app_name = "alerts"
urlpatterns = [
    path("", views.index_list, name="index"),
    path("create/", views.create, name="create"),
    path("edit/<int:pk>", views.edit, name="edit"),
    path("delete/<int:pk>", views.delete, name="delete"),
    path("help/", views.help, name="help"),
    path("test_notifications/", views.test_notifications, name="test_notifications"),
]
