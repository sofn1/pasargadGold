from django.urls import path
from .views import (WishlistView, WishlistDetailView, CartView, AddressView, AddressDetailView,
                    NotificationListView, OrderSummaryView, CustomerOrderHistoryView, CustomerProfileView,
                    CustomerRecommendedProductsView, SupportTicketListCreateView, TicketReplyListCreateView,
                    InvoiceDownloadView, AdminTicketReplyView, UnreadNotificationsView, CustomerTicketListView,
                    AdminReplyToTicketView, NotificationMarkReadView, CustomerSupportTicketListCreateView,
                    customer_dashboard_home)

from .views import (OrderHistoryPage, ProfilePage, RecommendedProductsPage,
                    WishlistPage, CartPage, AddressesPage, NotificationsPage, SupportTicketsPage, InvoicePage)

urlpatterns = [
    path('wishlist/', WishlistView.as_view(), name='wishlist-list-create'),
    path('wishlist/<int:pk>/', WishlistDetailView.as_view(), name='wishlist-delete'),
    path('addresses/', AddressView.as_view(), name='customer-addresses'),
    path('addresses/<int:pk>/', AddressDetailView.as_view(), name='customer-address-detail'),
    path('order-summary/', OrderSummaryView.as_view(), name='customer-order-summary'),
    path('orders/history/', CustomerOrderHistoryView.as_view(), name='customer-order-history'),
    path('orders/<int:order_id>/invoice/', InvoiceDownloadView.as_view(), name='invoice-download'),
    path('support-tickets/', SupportTicketListCreateView.as_view(), name='support-ticket-list-create'),
    path('support-tickets/replies/', TicketReplyListCreateView.as_view(), name='ticket-reply-list-create'),
    path("support/", CustomerSupportTicketListCreateView.as_view(), name="customer-support-list-create"),
    path('notifications/<int:pk>/read/', NotificationMarkReadView.as_view(), name='mark-notification-read'),
    path('notifications/unread/', UnreadNotificationsView.as_view(), name='unread-notifications'),
    path('notifications/', NotificationListView.as_view(), name='customer-notifications'),
    path('tickets/', CustomerTicketListView.as_view(), name='ticket-list'),
    path('tickets/<int:ticket_id>/reply/', AdminReplyToTicketView.as_view(), name='admin-reply-ticket'),
    path('cart/', CartView.as_view(), name='customer-cart'),
    path('profile/', CustomerProfileView.as_view(), name='customer-profile'),
    path('recommendations/', CustomerRecommendedProductsView.as_view(), name='customer-recommendations'),
    path('admin/tickets/<int:ticket_id>/reply/', AdminTicketReplyView.as_view(), name='admin-ticket-reply'),

    # Frontend templates
    path('dashboard/', customer_dashboard_home, name='customer_dashboard_home'),
    path("frontend/orders/", OrderHistoryPage.as_view(), name="frontend_order_history"),
    path("frontend/profile/", ProfilePage.as_view(), name="frontend_profile"),
    path("frontend/recommended/", RecommendedProductsPage.as_view(), name="frontend_recommended"),
    path("frontend/wishlist/", WishlistPage.as_view(), name="frontend_wishlist"),
    path("frontend/cart/", CartPage.as_view(), name="frontend_cart"),
    path("frontend/addresses/", AddressesPage.as_view(), name="frontend_addresses"),
    path("frontend/notifications/", NotificationsPage.as_view(), name="frontend_notifications"),
    path("frontend/support-tickets/", SupportTicketsPage.as_view(), name="frontend_support_tickets"),
    path("frontend/invoice/<int:order_id>/", InvoicePage.as_view(), name="frontend_invoice"),

]
