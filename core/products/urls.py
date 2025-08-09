# products/urls.py
from django.urls import path
from .views import (
    ProductCategoryListPage, ProductCategoryDetailPage,
    ProductListPage, ProductDetailPage, FeaturedProductsPage
)

urlpatterns = [
    # Categories (HTML)
    path("categories/", ProductCategoryListPage.as_view(), name="product_category_list"),
    path("categories/<str:pk>/", ProductCategoryDetailPage.as_view(), name="product_category_detail"),

    # Products (HTML)
    path("", ProductListPage.as_view(), name="product_list"),
    path("<int:pk>/", ProductDetailPage.as_view(), name="product_detail"),
    path("featured/", FeaturedProductsPage.as_view(), name="product_featured"),
]
