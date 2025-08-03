from django.urls import path
from .views import (
    ProductListCreateView, ProductDetailView,
    ProductCategoryListCreateView, ProductCategoryDetailView, FeaturedProductsView
)

urlpatterns = [
    # Categories
    path('categories/', ProductCategoryListCreateView.as_view(), name='category_list_create'),
    path('categories/<str:pk>/', ProductCategoryDetailView.as_view(), name='category_detail'),

    # Products
    path('', ProductListCreateView.as_view(), name='product_list_create'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('featured/', FeaturedProductsView.as_view(), name='featured-products'),
]
