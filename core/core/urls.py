from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('products/', include('products.urls')),
    path('blogs/', include('blogs.urls')),
    path('news/', include('news.urls')),
    path('comments/', include('comments.urls')),
    path('orders/', include('orders.urls')),
    path("banners", include("banners.urls")),
    path("heroes", include("heroes.urls")),

    path('accounts/', include('accounts.urls')),
    path('admin-dashboard/', include('admin_dashboard.urls')),
    path('writer/', include('writer_dashboard.urls')),
    path('seller/', include('seller_dashboard.urls', namespace='seller')),
    path('customer/', include('customer_dashboard.urls')),

    # ✅ FRONTEND PAGES
    path('', include('frontend.urls')),

]

