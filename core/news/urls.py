# news/urls.py
from django.urls import path
from .views import (
    NewsCategoryListPage,
    NewsCategoryDetailPage,
    NewsListPage,
    NewsDetailPage,
)

urlpatterns = [
    # Category pages (Mongo)
    path("categories/", NewsCategoryListPage.as_view(), name="news_category_list"),
    path("categories/<str:pk>/", NewsCategoryDetailPage.as_view(), name="news_category_detail"),

    # News pages (Postgres)
    path("", NewsListPage.as_view(), name="news_list"),
    path("<int:pk>/", NewsDetailPage.as_view(), name="news_detail"),
]
