from django.urls import path
from .views import (
    home, profile, cart, checkout,
    login_view, register,
    blog_list, blog_detail,
    news_list, news_detail,
    notifications, product_detail, product_list, add_to_cart, CustomerRegisterPage, SellerRegisterPage,
    WriterRegisterPage
)

urlpatterns = [
    path("", home, name="home"),
    path("profile/", profile, name="profile"),
    path("cart/", cart, name="cart"),
    path("checkout/", checkout, name="checkout"),
    path("login/", login_view, name="login"),
    path("register/", register, name="register"),
    path("product/<int:id>/", product_detail, name="product_detail"),
    path("products/", product_list, name="product_list"),
    path("blogs/", blog_list, name="blog_list"),
    path("blogs/<int:id>/", blog_detail, name="blog_detail"),
    path("news/", news_list, name="news_list"),
    path("news/<int:id>/", news_detail, name="news_detail"),
    path("notifications/", notifications, name="notifications"),
    path("add-to-cart/<int:id>/", add_to_cart, name="add_to_cart"),

    path('register/customer/', CustomerRegisterPage.as_view(), name='register_customer'),
    path('register/seller/', SellerRegisterPage.as_view(), name='register_seller'),
    path('register/writer/', WriterRegisterPage.as_view(), name='register_writer'),
]
