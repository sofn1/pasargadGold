# heroes/urls.py
from django.urls import path
from .views import HeroListView


urlpatterns = [
    path("heroes/", HeroListView.as_view()),
]
