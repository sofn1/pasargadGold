# admin_dashboard/urls.py
from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    # Dashboard Home
    path('', views.dashboard_home, name='admin_home'),

    # Categories
    path('categories/', views.CategoryListView.as_view(), name='admin_categories'),
    path('categories/create/', views.CategoryCreateView.as_view(), name='admin_category_create'),
    path('categories/<uuid:category_id>/edit/', views.category_edit_view, name='admin_category_edit'),
    path('categories/<uuid:category_id>/delete/', views.category_delete_view, name='admin_category_delete'),

    # Brands
    path("brands/", views.BrandListView.as_view(), name="admin_brands"),
    path("brands/create/", views.brand_create_view, name="admin_brand_create"),
    path("brands/<str:pk>/edit/", views.brand_edit_view, name="admin_brand_edit"),
    path("brands/<str:pk>/delete/", views.brand_delete_view, name="admin_brand_delete"),

    # Banners
    path('banners/', views.BannerListView.as_view(), name='admin_banners'),
    path('banners/create/', views.banner_create_view, name='admin_banner_create'),
    path('banners/<int:pk>/edit/', views.banner_edit_view, name='admin_banner_edit'),
    path('banners/<int:pk>/delete/', views.banner_delete_view, name='admin_banner_delete'),

    # Heros
    path('heroes/', views.HeroListView.as_view(), name='admin_heroes'),
    path('heroes/create/', views.hero_create_view, name='admin_hero_create'),
    path('heroes/<int:pk>/edit/', views.hero_edit_view, name='admin_hero_edit'),
    path('heroes/<int:pk>/delete/', views.hero_delete_view, name='admin_hero_delete'),

    # AJAX search APIs (staff-only)
    path('api/search/categories/', views.api_search_categories, name='api_search_categories'),
    path('api/search/blogs/', views.api_search_blogs, name='api_search_blogs'),
    path('api/search/news/', views.api_search_news, name='api_search_news'),
    path('api/search/products/', views.api_search_products, name='api_search_products'),
    path('api/get-product/<int:product_id>/', views.api_get_product_data, name='api_get_product'),

    # Products
    path('products/', views.ProductListView.as_view(), name='admin_products'),
    path('products/create/', views.product_create_view, name='admin_product_create'),
    path('products/<int:pk>/edit/', views.product_edit_view, name='admin_product_edit'),
    path('products/<int:pk>/delete/', views.product_delete_view, name='admin_product_delete'),

    # Writers
    path("writers/", views.admin_writers_list, name="admin_writers"),
    path("writers/create/", views.admin_writers_create, name="admin_writers_create"),
    path("writers/<int:pk>/edit/", views.admin_writers_edit, name="admin_writers_edit"),
    path("writers/<int:pk>/delete/", views.admin_writers_delete, name="admin_writers_delete"),

    # Sellers
    path("sellers/", views.admin_sellers_list, name="admin_sellers"),
    path("sellers/create/", views.admin_sellers_create, name="admin_sellers_create"),
    path("sellers/<int:pk>/edit/", views.admin_sellers_edit, name="admin_sellers_edit"),
    path("sellers/<int:pk>/delete/", views.admin_sellers_delete, name="admin_sellers_delete"),



    # Users
    path('users/', views.UserListView.as_view(), name='admin_users_list'),
    path('users/<int:pk>/', views.UserDetailView.as_view(), name='admin_user_detail'),

    # Blogs
    path('blogs/', views.AdminBlogListView.as_view(), name='admin_blogs'),
    path('blogs/create/', views.blog_create_view, name='admin_blog_create'),
    path('blogs/<int:pk>/edit/', views.blog_edit_view, name='admin_blog_edit'),
    path('blogs/<int:pk>/delete/', views.blog_delete_view, name='admin_blog_delete'),

    # News
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

    # Logs
    path('activity/', views.ActivityLogView.as_view(), name='admin_activity_logs'),

    # API
    path('api/stats/', views.api_stats_summary, name='admin_api_stats'),
]
