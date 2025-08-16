from django.shortcuts import render
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.decorators import admin_required, writer_required, seller_required, superadmin_required


@superadmin_required
def superadmin_dashboard_view(request):
    return render(request, 'superadmin_dashboard/dashboard.html')


@admin_required
def admin_dashboard_view(request):
    if request.user.is_superuser:
        return redirect('/superadmin-dashboard/')
    return render(request, 'admin_dashboard/dashboard.html')


@writer_required
def writer_dashboard_view(request):
    return render(request, 'writer_dashboard/dashboard.html')


@seller_required
def seller_dashboard_view(request):
    return render(request, 'seller_dashboard/dashboard.html')


class AdminSiteSummaryPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/summary.html"


class AdminSellersPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/sellers.html"


class AdminWritersPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/writers.html"


class AdminFlaggedCommentsPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/flagged_comments.html"


class AdminLowStockAlertsPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/low_stock.html"


class AdminFailedPaymentsPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/failed_payments.html"


class AdminCreateSellerPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/seller_create.html"


class AdminUpdateSellerPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/seller_update.html"


class AdminCreateAdminPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/admin_create.html"


class AdminLogsPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/admin_logs.html"


class AdminManageAdminsPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/manage_admins.html"


class AdminImpersonationPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/impersonation.html"


class AdminGrowthAnalyticsPage(LoginRequiredMixin, TemplateView):
    template_name = "admin_dashboard/growth_analytics.html"

