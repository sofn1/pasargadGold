from django.urls import path
from .views import (
    BlogCategoryListCreateView, BlogCategoryDetailView,
    BlogListCreateView, BlogDetailView
)

urlpatterns = [
    # Categories
    path('categories/', BlogCategoryListCreateView.as_view(), name='blog-category-list-create'),
    path('categories/<str:pk>/', BlogCategoryDetailView.as_view(), name='blog-category-detail'),

    # Blogs
    path('', BlogListCreateView.as_view(), name='blog_list_create'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_detail'),
]
