from django.urls import path
from .views import (SiteSummaryView, SellersListView, WritersListView, FlaggedContentView, LowStockAlertsView,
                    FailedPaymentsView, SellerCreateView, SellerUpdateDeleteView, WriterPermissionUpdateView,
                    AdminCreateView, ExportSellersExcelView, ExportWritersExcelView, ExportFlaggedCommentsExcelView,
                    ExportFilteredLogsExcelView, AdminLogsView, AdminActivitySummaryView, AdminManagementView,
                    InviteAdminView, ActivateAdminTokenView, AdminSuspendView, ImpersonateAdminView,
                    admin_dashboard_view, writer_dashboard_view, seller_dashboard_view, superadmin_dashboard_view)

from .views import (AdminSiteSummaryPage, AdminSellersPage, AdminWritersPage, AdminFlaggedCommentsPage,
                    AdminLowStockAlertsPage, AdminFailedPaymentsPage, AdminCreateSellerPage, AdminUpdateSellerPage,
                    AdminCreateAdminPage, AdminLogsPage, AdminManageAdminsPage, AdminImpersonationPage,
                    AdminGrowthAnalyticsPage)

urlpatterns = [
    path('site-summary/', SiteSummaryView.as_view()),
    path('sellers/', SellersListView.as_view()),
    path('writers/', WritersListView.as_view()),
    path('moderation/comments/', FlaggedContentView.as_view()),
    path('low-stock-alerts/', LowStockAlertsView.as_view()),
    path('failed-payments/', FailedPaymentsView.as_view()),
    path('sellers/create/', SellerCreateView.as_view()),
    path('sellers/<int:id>/update-delete/', SellerUpdateDeleteView.as_view()),
    path('writers/<int:writer_id>/permissions/', WriterPermissionUpdateView.as_view()),
    path('admins/create/', AdminCreateView.as_view()),
    path('export/sellers/', ExportSellersExcelView.as_view()),
    path('export/writers/', ExportWritersExcelView.as_view()),
    path('export/flagged-comments/', ExportFlaggedCommentsExcelView.as_view()),
    path('export/admin-logs/', ExportFilteredLogsExcelView.as_view()),
    path('logs/', AdminLogsView.as_view()),
    path('activity-summary/', AdminActivitySummaryView.as_view()),
    path('manage-admins/', AdminManagementView.as_view()),
    path('invite-admin/', InviteAdminView.as_view()),
    path('activate-admin-token/', ActivateAdminTokenView.as_view()),
    path('admin-suspend/', AdminSuspendView.as_view()),
    path('impersonate-admin/', ImpersonateAdminView.as_view()),


    path('', admin_dashboard_view, name='admin-dashboard'),
    path('superadmin-dashboard/', superadmin_dashboard_view, name='superadmin-dashboard'),
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
