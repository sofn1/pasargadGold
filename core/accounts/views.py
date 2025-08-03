from rest_framework import generics, permissions
from rest_framework.response import Response
from .models import Customer, Seller, Writer
from .permissions import IsSuperAdminOrAdmin, IsSuperAdminOnly
from accounts.serializers.customer import CustomerRegisterSerializer
from accounts.serializers.seller import SellerRegisterSerializer
from accounts.serializers.writer import WriterRegisterSerializer


# Register Customer - Anyone can register
class RegisterCustomerView(generics.CreateAPIView):
    serializer_class = CustomerRegisterSerializer
    permission_classes = [permissions.AllowAny]


# Register Seller - Only admin/superadmin
class RegisterSellerView(generics.CreateAPIView):
    serializer_class = SellerRegisterSerializer
    permission_classes = [IsSuperAdminOrAdmin]


# Register Writer - Only admin/superadmin
class RegisterWriterView(generics.CreateAPIView):
    serializer_class = WriterRegisterSerializer
    permission_classes = [IsSuperAdminOrAdmin]
