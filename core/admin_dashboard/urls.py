# admin_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.dashboard_home, name='admin_home'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='admin_categories'),
    path('categories/create/', views.category_create_view, name='admin_category_create'),
    path('categories/<str:category_id>/edit/', views.category_edit_view, name='admin_category_edit'),
    path('categories/<str:category_id>/delete/', views.category_delete_view, name='admin_category_delete'),

    # Users
    path('users/', views.UserListView.as_view(), name='admin_users_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='admin_user_detail'),

    # Blogs - CRUD
    path('blogs/', views.AdminBlogListView.as_view(), name='admin_blogs'),
    path('blogs/create/', views.blog_create_view, name='admin_blog_create'),
    path('blogs/<int:pk>/edit/', views.blog_edit_view, name='admin_blog_edit'),
    path('blogs/<int:pk>/delete/', views.blog_delete_view, name='admin_blog_delete'),

    # News - CRUD
    path('news/', views.AdminNewsListView.as_view(), name='admin_news'),
    path('news/create/', views.news_create_view, name='admin_news_create'),
    path('news/<int:pk>/edit/', views.news_edit_view, name='admin_news_edit'),
    path('news/<int:pk>/delete/', views.news_delete_view, name='admin_news_delete'),

    # Comments
    path('comments/', views.CommentModerationView.as_view(), name='admin_comments'),

    # Orders
    path('orders/', views.OrderListView.as_view(), name='admin_orders'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='admin_order_detail'),
    path('orders/<int:pk>/status/', views.update_order_status, name='admin_update_order_status'),

    # Media & Layout
    path('banners/', views.BannerListView.as_view(), name='admin_banners'),
    path('banners/create/', views.banner_create_view, name='admin_banner_create'),
    path('banners/<int:pk>/edit/', views.banner_edit_view, name='admin_banner_edit'),
    path('banners/<int:pk>/delete/', views.banner_delete_view, name='admin_banner_delete'),

    path('heroes/', views.HeroListView.as_view(), name='admin_heroes'),
    path('heroes/create/', views.hero_create_view, name='admin_hero_create'),
    path('heroes/<int:pk>/edit/', views.hero_edit_view, name='admin_hero_edit'),
    path('heroes/<int:pk>/delete/', views.hero_delete_view, name='admin_hero_delete'),

    path('brands/', views.BrandListView.as_view(), name='admin_brands'),
    path('brands/create/', views.brand_create_view, name='admin_brand_create'),
    path('brands/<int:pk>/edit/', views.brand_edit_view, name='admin_brand_edit'),
    path('brands/<int:pk>/delete/', views.brand_delete_view, name='admin_brand_delete'),

    path('products/', views.ProductListView.as_view(), name='admin_products'),
    path('products/create/', views.product_create_view, name='admin_product_create'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='admin_product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='admin_product_delete'),

    # Logs
    path('activity/', views.ActivityLogView.as_view(), name='admin_activity_logs'),

    # API
    path('api/stats/', views.api_stats_summary, name='admin_api_stats'),
]
