# core/banners/urls.py
from django.urls import path
from .views import BannerListView

urlpatterns = [
    path("banners/", BannerListView.as_view()),
]
