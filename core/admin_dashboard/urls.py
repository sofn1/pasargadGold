from django.urls import path
from .views import (AdminSiteSummaryPage, AdminSellersPage, AdminWritersPage, AdminFlaggedCommentsPage,
                    AdminLowStockAlertsPage, AdminFailedPaymentsPage, AdminCreateSellerPage, AdminUpdateSellerPage,
                    AdminCreateAdminPage, AdminLogsPage, AdminManageAdminsPage, AdminImpersonationPage,
                    AdminGrowthAnalyticsPage, admin_dashboard_view, writer_dashboard_view, seller_dashboard_view,
                    superadmin_dashboard_view)

urlpatterns = [
    path('superadmin-dashboard/', superadmin_dashboard_view, name='superadmin-dashboard'),
    path('', admin_dashboard_view, name='admin-dashboard'),
    path('writer-dashboard/', writer_dashboard_view, name='writer-dashboard'),
    path('seller-dashboard/', seller_dashboard_view, name='seller-dashboard'),

    path("summary/", AdminSiteSummaryPage.as_view(), name="admin_summary"),
    path("sellers/", AdminSellersPage.as_view(), name="admin_sellers"),
    path("writers/", AdminWritersPage.as_view(), name="admin_writers"),
    path("flagged-comments/", AdminFlaggedCommentsPage.as_view(), name="admin_flagged_comments"),
    path("low-stock/", AdminLowStockAlertsPage.as_view(), name="admin_low_stock"),
    path("failed-payments/", AdminFailedPaymentsPage.as_view(), name="admin_failed_payments"),
    path("sellers/create/", AdminCreateSellerPage.as_view(), name="admin_seller_create"),
    path("sellers/<int:id>/update/", AdminUpdateSellerPage.as_view(), name="admin_seller_update"),
    path("admins/create/", AdminCreateAdminPage.as_view(), name="admin_create"),
    path("admin-logs/", AdminLogsPage.as_view(), name="admin_logs"),
    path("manage-admins/", AdminManageAdminsPage.as_view(), name="admin_manage_admins"),
    path("impersonate/", AdminImpersonationPage.as_view(), name="admin_impersonate"),
    path("growth/", AdminGrowthAnalyticsPage.as_view(), name="admin_growth"),

]
