from .permissions import IsSuperAdminOrAdmin
from django.shortcuts import render, redirect
from rest_framework import generics, permissions
from django.contrib.auth import authenticate, login
from django.utils.http import url_has_allowed_host_and_scheme
from accounts.serializers.writer import WriterRegisterSerializer
from accounts.serializers.seller import SellerRegisterSerializer
from accounts.serializers.customer import CustomerRegisterSerializer


def login_user(request, role, template_name):
    if request.method == 'POST':
        phone = request.POST.get('phone_number')
        password = request.POST.get('password')
        next_url = request.GET.get('next') or '/'

        user = authenticate(request, phone_number=phone, password=password)

        if not user:
            return render(request, template_name, {'error': 'کاربر یافت نشد یا رمز عبور اشتباه است.'})

        # Role validation
        # if role == 'admin':
        #     if not hasattr(user, 'adminpermission'):
        #         return render(request, template_name, {'error': 'شما مدیر نیستید.'})
        if role == 'admin':
            if not hasattr(user, 'adminpermission'):
                if user.is_superuser:
                    # Create the admin permission on the fly
                    from accounts.models import AdminPermission
                    AdminPermission.objects.get_or_create(user=user, defaults={"is_superadmin": True})
                else:
                    return render(request, template_name, {'error': 'شما مدیر نیستید.'})
        elif role == 'writer':
            if not hasattr(user, 'writer'):
                return render(request, template_name, {'error': 'شما نویسنده نیستید.'})
        elif role == 'seller':
            if not hasattr(user, 'seller'):
                return render(request, template_name, {'error': 'شما فروشنده نیستید.'})

        # Successful login
        login(request, user)

        # Optional redirect to previous page if allowed
        if url_has_allowed_host_and_scheme(next_url, allowed_hosts={request.get_host()}):
            return redirect(next_url)

        # Redirects based on role
        if role == 'admin' and user.is_superuser:
            return redirect('/superadmin-dashboard/')
        elif role == 'admin':
            return redirect('/admin-dashboard/')
        elif role == 'writer':
            return redirect('/writer-dashboard/')
        elif role == 'seller':
            return redirect('/seller-dashboard/')

    # GET request
    return render(request, template_name)


def seller_login_view(request):
    return login_user(request, 'seller', 'seller_login.html')


def writer_login_view(request):
    return login_user(request, 'writer', 'writer_login.html')


def admin_login_view(request):
    return login_user(request, 'admin', 'admin_login.html')


def superadmin_login_view(request):
    return login_user(request, 'admin', 'admin_login.html')


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
