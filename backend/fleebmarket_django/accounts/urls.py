from django.urls import path

from . import views

app_name = 'accounts'
urlpatterns = [
    path('', views.Profile.as_view(), name='profile'),
    path('<int:pk>/', views.ProfileUpdate.as_view(), name='edit-profile'),
]
