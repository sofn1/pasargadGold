from django.contrib import messages
from django.shortcuts import render, redirect
from .utils import generate_excel_report, generate_csv_report
from django.contrib.auth.decorators import login_required, user_passes_test


def seller_summary_view(request):
    # Dummy data - replace with real DB queries
    seller_data = {
        'summary': {
            'درآمد کل': '120,000,000 تومان',
            'تعداد کل سفارش‌ها': 245,
            'سود خالص': '30,000,000 تومان',
            'میانگین ارزش سفارش': '489,000 تومان',
            'نرخ ترک سبد خرید': '38%',
            'مشتریان جدید': 89,
            'مشتریان بازگشتی': 156,
        },
        'top_products': [
            {'name': 'گوشواره طلای ۱۸ عیار', 'quantity_sold': 45, 'revenue': 22_500_000},
            {'name': 'انگشتر نامزدی طلا', 'quantity_sold': 38, 'revenue': 19_000_000},
            {'name': 'دستبند زنجیری طلا', 'quantity_sold': 32, 'revenue': 16_000_000},
        ],
        'low_stock_products': [
            {'name': 'گردنبند مروارید', 'current_stock': 2, 'min_stock': 5},
            {'name': 'ساعت طلای مردانه', 'current_stock': 1, 'min_stock': 3},
        ]
    }

    return render(request, 'seller_dashboard/summary.html', {'summary': seller_data})


def export_excel(request):
    seller_data = {
        'summary': {
            'درآمد کل': '120,000,000 تومان',
            'تعداد کل سفارش‌ها': 245,
            'سود خالص': '30,000,000 تومان',
            'میانگین ارزش سفارش': '489,000 تومان',
            'نرخ ترک سبد خرید': '38%',
            'مشتریان جدید': 89,
            'مشتریان بازگشتی': 156,
        },
        'top_products': [
            {'name': 'گوشواره طلای ۱۸ عیار', 'quantity_sold': 45, 'revenue': 22_500_000},
            {'name': 'انگشتر نامزدی طلا', 'quantity_sold': 38, 'revenue': 19_000_000},
        ],
        'low_stock_products': [
            {'name': 'گردنبند مروارید', 'current_stock': 2, 'min_stock': 5},
        ]
    }

    # ✅ Use phone_number instead of username
    user_identifier = request.user.phone_number

    return generate_excel_report(seller_data, filename="گزارش_فروشنده_" + user_identifier)


def export_csv(request):
    seller_data = {
        'summary': {
            'درآمد کل': '120,000,000 تومان',
            'تعداد کل سفارش‌ها': 245,
            'سود خالص': '30,000,000 تومان',
            'میانگین ارزش سفارش': '489,000 تومان',
        },
        'top_products': [
            {'name': 'گوشواره طلای ۱۸ عیار', 'quantity_sold': 45, 'revenue': 22_500_000},
            {'name': 'انگشتر نامزدی طلا', 'quantity_sold': 38, 'revenue': 19_000_000},
        ],
        'low_stock_products': [
            {'name': 'گردنبند مروارید', 'current_stock': 2, 'min_stock': 5},
        ]
    }

    # ✅ Use phone_number instead of username
    user_identifier = request.user.phone_number

    return generate_csv_report(seller_data, filename="گزارش_فروشنده_" + user_identifier)


def schedule_weekly_report(request):
    if request.method == "POST":
        messages.success(request, "گزارش هفتگی با موفقیت زمان‌بندی شد.")
    return redirect('seller:seller_summary')


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
