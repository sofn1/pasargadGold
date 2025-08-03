from django.urls import path
from .views import RegisterCustomerView, RegisterSellerView, RegisterWriterView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/customer/', RegisterCustomerView.as_view(), name='register_customer'),
    path('register/seller/', RegisterSellerView.as_view(), name='register_seller'),
    path('register/writer/', RegisterWriterView.as_view(), name='register_writer'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
