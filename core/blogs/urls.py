# blogs/urls.py
from django.urls import path
from .views import (
    BlogCategoryListPage,
    BlogCategoryDetailPage,
    BlogListPage,
    BlogDetailPage,
)

urlpatterns = [
    # Categories (HTML pages)
    path("categories/", BlogCategoryListPage.as_view(), name="blog_category_list"),
    path("categories/<str:pk>/", BlogCategoryDetailPage.as_view(), name="blog_category_detail"),

    # Blogs (HTML pages)
    path("", BlogListPage.as_view(), name="blog_list"),
    path("<int:pk>/", BlogDetailPage.as_view(), name="blog_detail"),
]
