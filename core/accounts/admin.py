from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Customer, Seller, Writer


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ("phone_number", "role", "is_active")
    ordering = ("phone_number",)
    search_fields = ("phone_number",)
    fieldsets = (
        (None, {"fields": ("phone_number", "password")}),
        ("Permissions", {"fields": ("role", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            'fields': ('phone_number', 'password1', 'password2', 'role'),
        }),
    )
