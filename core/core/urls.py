from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('api/accounts/', include('accounts.urls')),
    path('api/products/', include('products.urls')),
    path('api/blogs/', include('blogs.urls')),
    path('api/news/', include('news.urls')),
    path('api/comments/', include('comments.urls')),
    path('api/orders/', include('orders.urls')),
    path("api/banners", include("banners.urls")),
    path("api/heroes", include("heroes.urls")),

    path('api/admin/dashboard/', include('admin_dashboard.urls')),
    path('api/seller/dashboard/', include('seller_dashboard.urls')),
    path('api/writer/dashboard/', include('writer_dashboard.urls')),
    path('api/customer/dashboard/', include('customer_dashboard.urls')),

    path('admin-dashboard/', include('admin_dashboard.urls')),
    path('writer/dashboard/', include('writer_dashboard.urls')),
    path('seller/dashboard/', include('seller_dashboard.urls')),
    path('customer/dashboard/', include('customer_dashboard.urls')),

    # ✅ FRONTEND PAGES
    path('', include('frontend.urls')),

]

