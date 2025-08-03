from django.urls import path
from .views import (
    NewsCategoryListCreateView, NewsCategoryDetailView,
    NewsListCreateView, NewsDetailView
)

urlpatterns = [
    # Categories
    path('categories/', NewsCategoryListCreateView.as_view(), name='news-category-list-create'),
    path('categories/<str:pk>/', NewsCategoryDetailView.as_view(), name='news-category-detail'),

    # News
    path('', NewsListCreateView.as_view(), name='news_list_create'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
]
