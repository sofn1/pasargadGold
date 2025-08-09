# orders/urls.py
from django.urls import path
from .views import CartPage, CartItemRemoveView, CheckoutPage, ZarinpalVerifyView


urlpatterns = [
    path("cart/", CartPage.as_view(), name="orders_cart"),
    path("cart/remove/<int:pk>/", CartItemRemoveView.as_view(), name="orders_cart_remove"),
    path("checkout/", CheckoutPage.as_view(), name="orders_checkout"),
    path("verify/", ZarinpalVerifyView.as_view(), name="zarinpal_verify"),
]
