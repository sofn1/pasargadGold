# heroes/urls.py
from django.urls import path
from .views import HeroListPage

urlpatterns = [
    path("heroes/", HeroListPage.as_view(), name="heroes-list-page"),
]
