from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterCustomerView, RegisterSellerView, RegisterWriterView, seller_login_view, writer_login_view, \
    admin_login_view, customer_login, custom_logout_view

urlpatterns = [
    path('register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('register/seller/', RegisterSellerView.as_view(), name='register_seller'),
    path('register/writer/', RegisterWriterView.as_view(), name='register_writer'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('seller-login/', seller_login_view, name='seller-login'),
    path('writer-login/', writer_login_view, name='writer-login'),
    path('admin-login/', admin_login_view, name='admin-login'),
    path('customer-login/', customer_login, name='customer-login'),

    path('logout/', custom_logout_view, name='account_logout'),
]
