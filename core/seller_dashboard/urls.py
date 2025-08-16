from django.urls import path
from . import views
from .views import seller_dashboard_home

app_name = 'seller'

urlpatterns = [
    path("dashboard/", seller_dashboard_home, name="dashboard"),

    path('summary/', views.seller_summary_view, name='seller_summary'),
    path('revenue-time-series/', views.revenue_time_series_view, name='seller_revenue_time_series'),
    path('order-time-series/', views.order_time_series_view, name='seller_order_time_series'),
    path('profit-time-series/', views.profit_time_series_view, name='seller_profit_time_series'),
    path('top-products/', views.top_products_view, name='seller_top_products'),
    path('low-stock-products/', views.low_stock_products_view, name='seller_low_stock_products'),
    path('order-funnel/', views.order_funnel_view, name='seller_order_funnel'),
    path('geo-breakdown/', views.geo_breakdown_view, name='seller_geo_breakdown'),
    path('device-breakdown/', views.device_breakdown_view, name='seller_device_breakdown'),
    path('unfulfilled-orders/', views.unfulfilled_orders_view, name='seller_unfulfilled_orders'),
    path('system-health/', views.system_health_view, name='seller_system_health'),
    path('sales-by-channel/', views.sales_by_channel_view, name='seller_sales_by_channel'),

]
