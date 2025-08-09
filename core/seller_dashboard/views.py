from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda u: u.role == 'seller')
def seller_dashboard_home(request):
    return render(request, 'seller_dashboard/dashboard.html')


@login_required
def seller_summary_view(request):
    return render(request, 'seller_dashboard/summary.html')


@login_required
def revenue_time_series_view(request):
    return render(request, 'seller_dashboard/revenue_time_series.html')


@login_required
def order_time_series_view(request):
    return render(request, 'seller_dashboard/order_time_series.html')


@login_required
def profit_time_series_view(request):
    return render(request, 'seller_dashboard/profit_time_series.html')


@login_required
def top_products_view(request):
    return render(request, 'seller_dashboard/top_products.html')


@login_required
def low_stock_products_view(request):
    return render(request, 'seller_dashboard/low_stock_products.html')


@login_required
def order_funnel_view(request):
    return render(request, 'seller_dashboard/order_funnel.html')


@login_required
def geo_breakdown_view(request):
    return render(request, 'seller_dashboard/geo_breakdown.html')


@login_required
def device_breakdown_view(request):
    return render(request, 'seller_dashboard/device_breakdown.html')


@login_required
def unfulfilled_orders_view(request):
    return render(request, 'seller_dashboard/unfulfilled_orders.html')


@login_required
def system_health_view(request):
    return render(request, 'seller_dashboard/system_health.html')


@login_required
def sales_by_channel_view(request):
    return render(request, 'seller_dashboard/sales_by_channel.html')
