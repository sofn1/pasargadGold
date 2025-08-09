# core/banners/urls.py
from django.urls import path
from .views import BannerListPage

urlpatterns = [
    path("banners/", BannerListPage.as_view(), name="banners-list-page"),
]
