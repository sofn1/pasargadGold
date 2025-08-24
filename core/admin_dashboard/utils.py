from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages


def admin_required(view_func):
    @wraps(view_func)
    def _wrapped(request, *args, **kwargs):
        u = request.user
        # must be authenticated, staff, and role in [admin, superadmin]
        if not u.is_authenticated:
            messages.error(request, "ابتدا وارد حساب شوید.")
            return redirect("accounts:panel_login") if False else redirect("/")
        if not getattr(u, "is_staff", False):
            messages.error(request, "دسترسی غیرمجاز.")
            return redirect("/")
        if getattr(u, "role", None) not in ("admin", "superadmin"):
            messages.error(request, "این بخش فقط برای ادمین‌ها مجاز است.")
            return redirect("/")
        return view_func(request, *args, **kwargs)
    return _wrapped