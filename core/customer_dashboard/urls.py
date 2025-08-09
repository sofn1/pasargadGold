from django.urls import path
from .views import (OrderHistoryPage, ProfilePage, RecommendedProductsPage, customer_dashboard_home,
                    WishlistPage, CartPage, AddressesPage, NotificationsPage, SupportTicketsPage, InvoicePage)

urlpatterns = [
    path('dashboard/', customer_dashboard_home, name='customer_dashboard_home'),
    path("orders/", OrderHistoryPage.as_view(), name="frontend_order_history"),
    path("profile/", ProfilePage.as_view(), name="frontend_profile"),
    path("recommended/", RecommendedProductsPage.as_view(), name="frontend_recommended"),
    path("wishlist/", WishlistPage.as_view(), name="frontend_wishlist"),
    path("cart/", CartPage.as_view(), name="frontend_cart"),
    path("addresses/", AddressesPage.as_view(), name="frontend_addresses"),
    path("notifications/", NotificationsPage.as_view(), name="frontend_notifications"),
    path("support-tickets/", SupportTicketsPage.as_view(), name="frontend_support_tickets"),
    path("invoice/<int:order_id>/", InvoicePage.as_view(), name="frontend_invoice"),

]
