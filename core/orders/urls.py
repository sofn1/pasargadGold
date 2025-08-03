from django.urls import path
from .views import (
    CartItemView, CartItemDeleteView, CreateOrderView,
    PayWithZarinpal, ZarinpalVerify
)

urlpatterns = [
    path('cart/', CartItemView.as_view(), name='cart_list_create'),
    path('cart/<int:pk>/', CartItemDeleteView.as_view(), name='cart_delete'),
    path('create/', CreateOrderView.as_view(), name='create_order'),
    path('pay/<int:order_id>/', PayWithZarinpal.as_view(), name='pay_zarinpal'),
    path('verify/', ZarinpalVerify.as_view(), name='verify_zarinpal'),
]
