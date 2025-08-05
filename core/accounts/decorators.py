from functools import wraps
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


def role_required(role_attr):
    def decorator(view_func):
        @wraps(view_func)
        @login_required(login_url='/accounts/panel-login/')
        def _wrapped_view(request, *args, **kwargs):
            if not hasattr(request.user, role_attr):
                return redirect('/accounts/panel-login/?next=' + request.path)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def superadmin_required(view_func):
    @wraps(view_func)
    @login_required(login_url='/accounts/admin-login/')
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            print("⛔ BLOCKED: not superuser")
            return redirect('/admin-dashboard/')
        print("✅ ALLOWED: superuser access granted")
        return view_func(request, *args, **kwargs)
    return _wrapped_view


# Predefined shortcuts
# superuser_required = (superadmin_required('admin'))
admin_required = role_required('adminpermission')
writer_required = role_required('writer')
seller_required = role_required('seller')
