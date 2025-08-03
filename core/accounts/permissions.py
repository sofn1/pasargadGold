from rest_framework.permissions import BasePermission


class IsSuperAdminOnly(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'superadmin'


class IsSuperAdminOrAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['superadmin', 'admin']


class IsAdminOrSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and
            request.user.role in ["admin", "superadmin"]
        )


