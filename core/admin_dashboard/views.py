# admin_dashboard/views.py
import os
import json
from django.views import View
from django.urls import reverse
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models.functions import Cast
from django.contrib.auth import get_user_model
from django.core.files.base import ContentFile
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db.models import Sum, Q, CharField, Count
from django.core.files.storage import default_storage
from django.views.generic import ListView, DetailView
from django.http import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test

from tags.models import Tag
from tags.forms import TagForm
from heroes.models import Hero
from datetime import timedelta
from accounts.models import User
from banners.models import Banner
from news.models.news import News
from .utils import admin_required
from blogs.models.blog import Blog
from comments.models import Comment
from logs.models import AdminActionLog
from categories.models import Category
from products.models.brand import Brand
from orders.models import Order, CartItem
from payments.models import FailedPayment
from products.models.product import Product
from accounts.models import Writer, WriterPermission, Seller
from .forms import (BlogForm, NewsForm, BannerForm, HeroForm, BrandForm, ProductForm, CategoryForm, CategoryCreateForm,
                    AdminCreateWriterForm, AdminUpdateWriterForm, AdminCreateSellerForm, AdminUpdateSellerForm, )

# Shortcut to check if user is staff
staff_required = user_passes_test(lambda u: u.is_staff, login_url='/accounts/login/')
method_staff_required = method_decorator(staff_required, name='dispatch')

User = get_user_model()


# =====================================
# DASHBOARD OVERVIEW
# =====================================

@staff_required
def dashboard_home(request):
    """Main admin dashboard with key metrics and charts."""
    now = timezone.now()
    start_of_week = now - timedelta(days=7)

    # Stats
    total_users = User.objects.count()
    active_users = User.objects.filter(last_login__gte=start_of_week).count()
    total_products = Product.objects.filter(is_active=True).count()
    total_blogs = Blog.objects.count()
    total_news = News.objects.count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0
    pending_orders = Order.objects.filter(status='pending').count()
    failed_payments = FailedPayment.objects.filter(created_at__gte=start_of_week).count()
    total_comments = Comment.objects.count()
    flagged_comments = Comment.objects.filter(status='flagged').count()

    # Recent Orders (last 10)
    recent_orders = Order.objects.all().order_by('-created_at')[:10]

    # Sales Chart Data (last 7 days)
    dates = [(start_of_week + timedelta(days=i)).date() for i in range(8)]
    sales_data = []
    for date in dates:
        day_start = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
        day_end = day_start + timedelta(days=1)
        daily_sales = Order.objects.filter(
            status='paid',
            created_at__range=(day_start, day_end)
        ).aggregate(Sum('total_price'))['total_price__sum'] or 0
        sales_data.append(int(daily_sales))

    context = {
        'total_users': total_users,
        'active_users': active_users,
        'total_products': total_products,
        'total_blogs': total_blogs,
        'total_news': total_news,
        'total_orders': total_orders,
        'total_revenue': total_revenue,
        'pending_orders': pending_orders,
        'failed_payments': failed_payments,
        'total_comments': total_comments,
        'flagged_comments': flagged_comments,
        'recent_orders': recent_orders,
        'chart_labels': [d.isoformat() for d in dates],
        'chart_data': sales_data,
    }
    return render(request, 'admin_dashboard/home.html', context)


# =====================================
# USER MANAGEMENT
# =====================================

class UserListView(ListView):
    model = User
    template_name = 'admin_dashboard/users/list.html'
    context_object_name = 'users'
    paginate_by = 20

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        query = self.request.GET.get('q')
        # Use last_login instead of date_joined
        qs = User.objects.all().order_by('-last_login')
        if query:
            qs = qs.filter(phone_number__icontains=query) | qs.filter(full_name__icontains=query)
        return qs


class UserDetailView(DetailView):
    model = User
    template_name = 'admin_dashboard/users/detail.html'
    context_object_name = 'user_obj'

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        context['user_orders'] = Order.objects.filter(user=user)
        context['user_blogs'] = Blog.objects.filter(writer=user)
        context['user_news'] = News.objects.filter(writer=user)
        context['user_cart_items'] = CartItem.objects.filter(user=user)
        return context


# =====================================
# CONTENT MODERATION
# =====================================

class CommentModerationView(ListView):
    model = Comment
    template_name = 'admin_dashboard/content/comments.html'
    context_object_name = 'comments'
    paginate_by = 20

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        status = self.request.GET.get('status', 'all')
        qs = Comment.objects.select_related('user').prefetch_related('content_object')
        if status == 'flagged':
            qs = qs.filter(status='flagged')
        elif status == 'hidden':
            qs = qs.filter(status='hidden')
        else:
            qs = qs.exclude(status='hidden')  # Default: show visible + flagged
        return qs.order_by('-created_at')

    def post(self, request, *args, **kwargs):
        comment_id = request.POST.get('comment_id')
        action = request.POST.get('action')  # hide, show, delete
        comment = get_object_or_404(Comment, id=comment_id)

        if action == 'hide':
            comment.status = 'hidden'
            log_action = "Hide comment"
        elif action == 'show':
            comment.status = 'visible'
            log_action = "Show comment"
        elif action == 'delete':
            comment.delete()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Deleted comment",
                details=f"Deleted comment ID {comment_id} by {comment.user.phone_number}"
            )
            return redirect('admin_dashboard:comments')
        else:
            return JsonResponse({'error': 'Invalid action'}, status=400)

        comment.save()
        AdminActionLog.objects.create(
            admin=request.user,
            action=log_action,
            details=f"Comment ID {comment_id} set to {comment.status}"
        )
        return redirect('admin_dashboard:comments')


# =====================================
# E-COMMERCE MANAGEMENT
# =====================================

class OrderListView(ListView):
    model = Order
    template_name = 'admin_dashboard/orders/list.html'
    context_object_name = 'orders'
    paginate_by = 20

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        status = self.request.GET.get('status')
        qs = Order.objects.select_related('user').all().order_by('-created_at')
        if status:
            qs = qs.filter(status=status)
        return qs


class OrderDetailView(DetailView):
    model = Order
    template_name = 'admin_dashboard/orders/detail.html'
    context_object_name = 'order'

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def update_order_status(request, pk):
    if not request.user.is_staff:
        return JsonResponse({'error': 'Permission denied'}, status=403)

    order = get_object_or_404(Order, pk=pk)
    new_status = request.POST.get('status')
    valid_statuses = [choice[0] for choice in Order.STATUS_CHOICES]

    if new_status not in valid_statuses:
        return JsonResponse({'error': 'Invalid status'}, status=400)

    old_status = order.status
    order.status = new_status
    order.save()

    AdminActionLog.objects.create(
        admin=request.user,
        action="Update Order Status",
        details=f"Order {order.id}: {old_status} → {new_status}"
    )

    return JsonResponse({'success': True, 'new_status': new_status})


# =====================================
# MEDIA & LAYOUT MANAGEMENT
# =====================================

class BannerListView(ListView):
    model = Banner
    template_name = 'admin_dashboard/media/banners.html'
    context_object_name = 'banners'


class HeroListView(ListView):
    model = Hero
    template_name = 'admin_dashboard/media/heroes.html'
    context_object_name = 'heroes'


class BrandListView(ListView):
    model = Brand
    template_name = 'admin_dashboard/products/brands.html'
    context_object_name = 'brands'


try:
    # Optional fuzzy search if Postgres + pg_trgm is available
    from django.contrib.postgres.search import TrigramSimilarity

    HAS_TRIGRAM = True
except Exception:
    HAS_TRIGRAM = False


@method_staff_required
class ProductListView(ListView):
    model = Product
    template_name = 'admin_dashboard/products/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        qs = (
            Product.objects
            .select_related('brand')
            .prefetch_related('categories')
            .order_by('-created_at')
        )

        q = (self.request.GET.get('q') or '').strip()
        field = (self.request.GET.get('field') or '').strip()
        status = (self.request.GET.get('status') or '').strip()

        # Status filter
        if field == 'status' and status in ('active', 'inactive'):
            qs = qs.filter(is_active=(status == 'active'))

        # Name / English name / default (both with fuzzy)
        elif field in ('', 'name', 'english_name'):
            if q:
                if HAS_TRIGRAM:
                    # fuzzy similarity on selected field(s)
                    if field == 'name':
                        qs = qs.annotate(sim=TrigramSimilarity('name', q)).filter(
                            Q(sim__gte=0.2) | Q(name__icontains=q)).order_by('-sim', '-created_at')
                    elif field == 'english_name':
                        qs = qs.annotate(sim=TrigramSimilarity('english_name', q)).filter(
                            Q(sim__gte=0.2) | Q(english_name__icontains=q)).order_by('-sim', '-created_at')
                    else:
                        # both fields
                        qs = qs.annotate(
                            sim_name=TrigramSimilarity('name', q),
                            sim_en=TrigramSimilarity('english_name', q),
                        ).filter(
                            Q(sim_name__gte=0.2) | Q(sim_en__gte=0.2) | Q(name__icontains=q) | Q(
                                english_name__icontains=q)
                        ).order_by('-sim_name', '-sim_en', '-created_at')
                else:
                    # fallback icontains
                    if field == 'name':
                        qs = qs.filter(name__icontains=q)
                    elif field == 'english_name':
                        qs = qs.filter(english_name__icontains=q)
                    else:
                        qs = qs.filter(Q(name__icontains=q) | Q(english_name__icontains=q))

        # Category (name / english_name / slug)
        elif field == 'category' and q:
            qs = qs.filter(
                Q(categories__name__icontains=q) |
                Q(categories__english_name__icontains=q) |
                Q(categories__slug__icontains=q)
            ).distinct()

        # Brand
        elif field == 'brand' and q:
            qs = qs.filter(brand__name__icontains=q)

        # Price: supports "min-max", ">n", "<n", or exact "n"
        elif field == 'price' and q:
            s = q.replace(',', '').replace(' ', '')
            if '-' in s:
                try:
                    lo, hi = s.split('-', 1)
                    lo = int(lo) if lo else None
                    hi = int(hi) if hi else None
                    if lo is not None and hi is not None:
                        qs = qs.filter(price__gte=lo, price__lte=hi)
                    elif lo is not None:
                        qs = qs.filter(price__gte=lo)
                    elif hi is not None:
                        qs = qs.filter(price__lte=hi)
                except ValueError:
                    pass
            elif s.startswith('>'):
                try:
                    qs = qs.filter(price__gt=int(s[1:]))
                except ValueError:
                    pass
            elif s.startswith('<'):
                try:
                    qs = qs.filter(price__lt=int(s[1:]))
                except ValueError:
                    pass
            else:
                try:
                    qs = qs.filter(price=int(s))
                except ValueError:
                    pass

        # Features (search in keys/values by casting JSON to text)
        elif field == 'features' and q:
            # Cast JSONField to text for icontains search (Postgres)
            qs = qs.annotate(features_text=Cast('features', CharField())).filter(features_text__icontains=q)

        return qs


# =====================================
# LOGS & ACTIVITY
# =====================================

class ActivityLogView(ListView):
    model = AdminActionLog
    template_name = 'admin_dashboard/logs/activity.html'
    context_object_name = 'logs'
    paginate_by = 50

    def get_queryset(self):
        return AdminActionLog.objects.select_related('admin').order_by('-timestamp')


# =====================================
# API-like JSON Endpoints (for charts)
# =====================================

@staff_required
def api_stats_summary(request):
    """Returns JSON summary for dynamic dashboards."""
    now = timezone.now()
    week_ago = now - timedelta(days=7)

    data = {
        'users': {
            'total': User.objects.count(),
            'active_week': User.objects.filter(last_login__gte=week_ago).count(),
        },
        'orders': {
            'total': Order.objects.count(),
            'paid': Order.objects.filter(status='paid').count(),
            'revenue': float(
                Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0),
        },
        'content': {
            'blogs': Blog.objects.count(),
            'news': News.objects.count(),
            'products': Product.objects.filter(is_active=True).count(),
        },
        'comments': {
            'total': Comment.objects.count(),
            'flagged': Comment.objects.filter(status='flagged').count(),
        }
    }
    return JsonResponse(data)


# =====================================
# CATEGORY VIEW
# =====================================

@method_decorator(login_required, name="dispatch")
class CategoryListView(View):
    template_name = "admin_dashboard/categories/list.html"

    def get(self, request, *args, **kwargs):
        def dfs(node: Category, level: int, parent_name: str | None):
            rows.append({
                "id": str(node.id),
                "name": node.name,
                "slug": node.slug,
                "parent_name": parent_name,
                "children_count": node.children.filter(is_active=True).count(),
                "level": level,
            })
            for child in node.children.filter(is_active=True).order_by("name"):
                dfs(child, level + 2, node.name)

        roots = Category.objects.filter(is_active=True, parent__isnull=True).order_by("name")
        rows: list[dict] = []
        for r in roots:
            dfs(r, level=0, parent_name=None)

        return render(request, self.template_name, {
            "flat_rows": rows,
            "categories": rows,
            "rows": rows,
        })


@method_decorator(login_required, name="dispatch")
class CategoryCreateView(View):
    template_name = "admin_dashboard/categories/create.html"

    def get(self, request, *args, **kwargs):
        parent_id = request.GET.get("parent_id")
        initial = {"is_active": True}
        if parent_id:
            initial["parent"] = Category.objects.filter(id=parent_id).first()
        form = CategoryCreateForm(initial=initial)
        parent = Category.objects.filter(id=parent_id).first() if parent_id else None
        return render(request, self.template_name, {"form": form, "parent": parent})

    def post(self, request, *args, **kwargs):
        form = CategoryCreateForm(request.POST, request.FILES)
        if not form.is_valid():
            parent = form.cleaned_data.get("parent") if "parent" in form.cleaned_data else None
            return render(request, self.template_name, {"form": form, "parent": parent})

        obj = form.save()  # slug is auto-managed in model.save()
        AdminActionLog.objects.create(
            admin=request.user,
            action="Create Category",
            details=f"Created category '{obj.name}' (ID: {obj.id})"
        )
        messages.success(request, "دسته با موفقیت ایجاد شد.")
        return redirect(reverse("admin_dashboard:admin_categories"))


@staff_required
def category_edit_view(request, category_id):
    cat = get_object_or_404(Category, id=category_id)

    if request.method == "POST":
        form = CategoryForm(request.POST, request.FILES, instance=cat)
        if form.is_valid():
            old_parent = cat.parent_id
            obj = form.save()  # saves image + is_active correctly
            AdminActionLog.objects.create(
                admin=request.user,
                action="Update Category",
                details=f"Updated category '{obj.name}' (ID: {obj.id}). Parent changed: {old_parent} → {obj.parent_id}"
            )
            messages.success(request, "دسته با موفقیت بروزرسانی شد.")
            return redirect('admin_dashboard:admin_categories')
    else:
        form = CategoryForm(instance=cat)

    # For templates expecting dict-like `category`
    category_ctx = {
        "id": str(cat.id),
        "name": cat.name,
        "englishName": cat.english_name,
        "parent_id": str(cat.parent_id) if cat.parent_id else "",
        "slug": cat.slug,
        "image_url": cat.image.url if cat.image else "",
        "is_active": cat.is_active,
    }
    return render(request, "admin_dashboard/categories/edit.html", {
        "form": form,
        "category": category_ctx,
    })


@staff_required
def category_delete_view(request, category_id):
    cat = get_object_or_404(Category, id=category_id)
    if request.method == "POST":
        name = cat.name
        cat.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        messages.success(request, f"دسته «{name}» حذف شد.")
        return redirect('admin_dashboard:admin_categories')
    return render(request, "admin_dashboard/categories/confirm_delete.html",
                  {"category": cat, "children_count": cat.children.count()})


# =====================================
# ALL CRUDs OF THE MODELS
# =====================================

# --- BLOG CRUD ---
def _prepare_blog_form_for_admin(form, *, instance=None):
    """
    - Hide/remove author fields from the form so user cannot edit them
    - Remove raw category_id field (we'll use UI field 'product_category' instead)
    - Inject product_category ModelChoiceField on the instance
    """
    # Remove fields if they exist
    for f in ("writer", "writer_name", "writer_profile", "category_id"):
        if f in form.fields:
            del form.fields[f]

    # Inject product_category (single select)
    form.fields["product_category"] = _forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("name"),
        label="دسته‌بندی محصول",
        required=True,
        widget=_forms.Select(attrs={"class": "form-select"})
    )

    # Preselect current category on edit
    if instance and getattr(instance, "category_id", None):
        try:
            form.initial["product_category"] = Category.objects.filter(pk=instance.category_id).first()
        except Exception:
            pass

    return form


def _derive_writer_name(user):
    # Try typical full name fallbacks
    try:
        if hasattr(user, "get_full_name") and callable(user.get_full_name):
            fn = (user.get_full_name() or "").strip()
            if fn:
                return fn
    except Exception:
        pass
    full_name = f"{getattr(user, 'first_name', '')} {getattr(user, 'last_name', '')}".strip()
    if full_name:
        return full_name
    return getattr(user, "username", None) or getattr(user, "email", "") or "user"


def _derive_writer_profile_url(user):
    """
    Best-effort to pull a profile image/url from common related profiles.
    If none found, returns empty string. This keeps your model unchanged.
    """
    try:
        # Try common related objects (customize if you have a definitive one)
        for rel in ("profile", "customer", "writer", "seller"):
            obj = getattr(user, rel, None)
            if not obj:
                continue
            # direct URL field
            if hasattr(obj, "profile_image") and getattr(obj, "profile_image"):
                img = getattr(obj, "profile_image")
                return getattr(img, "url", "") or str(img)
            # generic image field named 'image'
            if hasattr(obj, "image") and getattr(obj, "image"):
                img = getattr(obj, "image")
                return getattr(img, "url", "") or str(img)
            # generic URL field
            if hasattr(obj, "profile_url") and getattr(obj, "profile_url"):
                return getattr(obj, "profile_url")
    except Exception:
        pass
    return ""


@method_decorator(login_required, name="dispatch")
class BlogListView(ListView):
    model = Blog
    template_name = 'admin_dashboard/content/blogs.html'
    context_object_name = 'blogs'
    paginate_by = 15

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


@method_decorator(staff_required, name='dispatch')
class AdminBlogListView(ListView):
    model = Blog
    template_name = 'admin_dashboard/blogs/list.html'
    context_object_name = 'blogs'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q', '')
        qs = Blog.objects.select_related('writer').all().order_by('-publish_time')
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(english_name__icontains=q))
        return qs


@method_decorator(login_required, name="dispatch")
class BlogBuilderCreateView(View):
    template_name = "admin_dashboard/blogs/builder_create.html"

    def get(self, request):
        form = BlogForm()
        form = _prepare_blog_form_for_admin(form)
        return render(request, self.template_name, {"form": form, "title": "ایجاد بلاگ"})

    @transaction.atomic
    def post(self, request):
        # Normalize rel_* arrays if posted from JS
        for key in ["rel_news", "rel_blogs", "rel_products"]:
            if isinstance(request.POST.get(key), list):
                request.POST = request.POST.copy()
                request.POST[key] = json.dumps(request.POST.getlist(key))

        form = BlogForm(request.POST, request.FILES)
        form = _prepare_blog_form_for_admin(form)

        if form.is_valid():
            blog = form.save(commit=False)

            # ✅ author fields from the logged-in user
            user = request.user
            blog.writer = user
            blog.writer_name = _derive_writer_name(user)
            blog.writer_profile = _derive_writer_profile_url(user)

            # ✅ category_id from product_category UI
            product_category = form.cleaned_data.get("product_category")
            if product_category:
                blog.category_id = str(product_category.pk)

            blog.save()  # save before M2M

            # ✅ tags (M2M) — either from BlogForm's own field or our injected one
            tags_qs = form.cleaned_data.get("tags")
            if tags_qs is not None:
                blog.tags.set(tags_qs)

            messages.success(request, "وبلاگ با موفقیت ایجاد شد.")
            return redirect("admin_dashboard:admin_blogs")

        return render(request, self.template_name, {"form": form, "title": "ایجاد بلاگ"})


@method_decorator(login_required, name="dispatch")
class AdminBlogEditView(View):
    template_name = "admin_dashboard/blogs/builder_create.html"  # reuse the builder template

    def get(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)
        form = BlogForm(instance=blog)
        form = _prepare_blog_form_for_admin(form, instance=blog)
        return render(request, self.template_name, {
            "form": form,
            "title": "ویرایش بلاگ",
            "blog": blog,
            "is_edit": True,
        })

    @transaction.atomic
    def post(self, request, pk):
        blog = get_object_or_404(Blog, pk=pk)

        # Normalize rel_* arrays if posted from JS
        for key in ["rel_news", "rel_blogs", "rel_products"]:
            if isinstance(request.POST.get(key), list):
                request.POST = request.POST.copy()
                request.POST[key] = json.dumps(request.POST.getlist(key))

        form = BlogForm(request.POST, request.FILES, instance=blog)
        form = _prepare_blog_form_for_admin(form, instance=blog)

        if form.is_valid():
            blog = form.save(commit=False)

            # ❌ do NOT allow changing authorship on edit
            blog.writer = blog.writer
            blog.writer_name = blog.writer_name
            blog.writer_profile = blog.writer_profile

            # ✅ update category_id from UI
            product_category = form.cleaned_data.get("product_category")
            if product_category:
                blog.category_id = str(product_category.pk)

            blog.save()

            # ✅ tags
            tags_qs = form.cleaned_data.get("tags")
            if tags_qs is not None:
                blog.tags.set(tags_qs)

            messages.success(request, "وبلاگ با موفقیت به‌روزرسانی شد.")
            return redirect("admin_dashboard:admin_blogs")

        return render(request, self.template_name, {
            "form": form,
            "title": "ویرایش بلاگ",
            "blog": blog,
            "is_edit": True,
        })


@csrf_exempt
def grapes_asset_upload(request):
    # Handles asset uploads from GrapesJS Asset Manager
    if request.method != "POST" or not request.FILES:
        return HttpResponseBadRequest("No file uploaded")
    files = request.FILES.getlist("files")
    urls = []
    media_root = settings.MEDIA_ROOT
    subdir = os.path.join("blogs", "content")
    os.makedirs(os.path.join(media_root, subdir), exist_ok=True)

    for f in files:
        path = os.path.join(subdir, f.name)
        full = os.path.join(media_root, path)
        with open(full, "wb+") as dest:
            for chunk in f.chunks():
                dest.write(chunk)
        urls.append(settings.MEDIA_URL + path)

    # Grapes expects { data: [{src: "..."}] }
    return JsonResponse({"data": [{"src": u} for u in urls]})


@staff_required
def blog_delete_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        name = blog.name
        blog.delete()
        AdminActionLog.objects.create(
            admin=request.user,
            action="Delete Blog",
            details=f"Deleted blog '{name}' (ID: {pk})"
        )
        return JsonResponse({'success': True})
    return render(request, 'admin_dashboard/blogs/confirm_delete.html', {'blog': blog})


# --- NEWS CRUD ---
class NewsListView(ListView):
    model = News
    template_name = 'admin_dashboard/content/news.html'
    context_object_name = 'news_list'
    paginate_by = 15

    @method_staff_required
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        # Optional: Order by publish time, newest first
        return News.objects.all().order_by('-publish_time')


@method_decorator(staff_required, name='dispatch')
class AdminNewsListView(ListView):
    model = News
    template_name = 'admin_dashboard/news/list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = News.objects.select_related('writer').all().order_by('-publish_time')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(english_name__icontains=q)
        return qs


@staff_required
def news_create_view(request):
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Create News",
                details=f"Created news '{news.name}' (ID: {news.id})"
            )
            return redirect('admin_dashboard:news')
    else:
        form = NewsForm()
    return render(request, 'admin_dashboard/news/form.html', {'form': form, 'title': 'Create News'})


@staff_required
def news_edit_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == "POST":
        form = NewsForm(request.POST, request.FILES, instance=news)
        if form.is_valid():
            news = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Update News",
                details=f"Updated news '{news.name}' (ID: {news.id})"
            )
            return redirect('admin_dashboard:news')
    else:
        form = NewsForm(instance=news)
    return render(request, 'admin_dashboard/news/form.html',
                  {'form': form, 'title': f'Edit News: {news.name}', 'news': news})


@staff_required
def news_delete_view(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.method == "POST":
        name = news.name
        news.delete()
        AdminActionLog.objects.create(
            admin=request.user,
            action="Delete News",
            details=f"Deleted news '{name}' (ID: {pk})"
        )
        return JsonResponse({'success': True})
    return render(request, 'admin_dashboard/news/confirm_delete.html', {'news': news})


# --- BANNER CRUD ---

@method_staff_required
class BannerListView(ListView):
    model = Banner
    template_name = 'admin_dashboard/banners/list.html'
    context_object_name = 'banners'
    paginate_by = 10


@staff_required
def banner_create_view(request):
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES)
        if form.is_valid():
            banner = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Create Banner",
                details=f"Banner '{banner.title}' created at position {banner.position}"
            )
            return redirect('admin_dashboard:admin_banners')  # <- matches your urls.py
    else:
        form = BannerForm()
    return render(request, 'admin_dashboard/banners/form.html', {'form': form, 'title': 'ایجاد بنر'})


@staff_required
def banner_edit_view(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        form = BannerForm(request.POST, request.FILES, instance=banner)
        if form.is_valid():
            banner = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Update Banner",
                details=f"Updated banner '{banner.title}'"
            )
            return redirect('admin_dashboard:admin_banners')
    else:
        form = BannerForm(instance=banner)
    return render(request, 'admin_dashboard/banners/form.html',
                  {'form': form, 'title': f'ویرایش بنر: {getattr(banner, "title", "")}'})


@staff_required
def banner_delete_view(request, pk):
    banner = get_object_or_404(Banner, pk=pk)
    if request.method == "POST":
        name = getattr(banner, "title", str(banner.pk))
        banner.delete()
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        messages.success(request, f"بنر «{name}» حذف شد.")
        return redirect('admin_dashboard:admin_banners')  # ← fix
    return render(request, 'admin_dashboard/banners/confirm_delete.html', {'banner': banner})


# --- HERO CRUD ---

@method_staff_required
class HeroListView(ListView):
    model = Hero
    template_name = 'admin_dashboard/heroes/list.html'
    context_object_name = 'heroes'
    paginate_by = 10


@staff_required
def hero_create_view(request):
    if request.method == "POST":
        form = HeroForm(request.POST, request.FILES)
        if form.is_valid():
            hero = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Create Hero",
                details=f"Hero '{getattr(hero, 'title', hero.pk)}' created"
            )
            return redirect('admin_dashboard:admin_heroes')  # ← FIX
    else:
        form = HeroForm()
    return render(request, 'admin_dashboard/heroes/form.html', {'form': form, 'title': 'ایجاد هیرو'})


@staff_required
def hero_edit_view(request, pk):
    hero = get_object_or_404(Hero, pk=pk)
    if request.method == "POST":
        form = HeroForm(request.POST, request.FILES, instance=hero)
        if form.is_valid():
            hero = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Update Hero",
                details=f"Updated hero '{getattr(hero, 'title', hero.pk)}'"
            )
            return redirect('admin_dashboard:admin_heroes')  # ← FIX
    else:
        form = HeroForm(instance=hero)
    return render(request, 'admin_dashboard/heroes/form.html',
                  {'form': form, 'title': f'ویرایش هیرو: {getattr(hero, "title", "")}'})


@staff_required
def hero_delete_view(request, pk):
    hero = get_object_or_404(Hero, pk=pk)
    if request.method == "POST":
        title = getattr(hero, "title", str(hero.pk))
        hero.delete()
        AdminActionLog.objects.create(
            admin=request.user,
            action="Delete Hero",
            details=f"Deleted hero '{title}' (ID: {pk})"
        )
        # AJAX path (used by the modal)
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        # Fallback full redirect
        messages.success(request, f"هیرو «{title}» حذف شد.")
        return redirect('admin_dashboard:admin_heroes')

    # GET → confirm page (in case someone hits the URL directly)
    return render(request, 'admin_dashboard/heroes/confirm_delete.html', {'hero': hero})


# --- BRAND CRUD ---

@method_staff_required
class BrandListView(ListView):
    model = Brand
    template_name = 'admin_dashboard/brands/list.html'
    context_object_name = 'brands'
    paginate_by = 15


@staff_required
def brand_create_view(request):
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES)
        if form.is_valid():
            brand = form.save()
            AdminActionLog.objects.create(
                admin=request.user, action="Create Brand",
                details=f"Brand '{brand.name}' created"
            )
            messages.success(request, "برند با موفقیت ایجاد شد.")
            return redirect('admin_dashboard:admin_brands')
    else:
        form = BrandForm()
    # pass brand=None so the partial knows it's create mode
    return render(request, 'admin_dashboard/brands/form.html',
                  {'form': form, 'title': 'ایجاد برند', 'brand': None})


@staff_required
def brand_edit_view(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == "POST":
        form = BrandForm(request.POST, request.FILES, instance=brand)
        if form.is_valid():
            # image is optional on edit (form handles required=False)
            # If the user didn't upload, Django keeps the existing file automatically.
            brand = form.save()
            AdminActionLog.objects.create(
                admin=request.user, action="Update Brand",
                details=f"Updated brand '{brand.name}'"
            )
            messages.success(request, "برند با موفقیت ویرایش شد.")
            return redirect('admin_dashboard:admin_brands')
    else:
        form = BrandForm(instance=brand)

    return render(request, 'admin_dashboard/brands/form.html',
                  {'form': form, 'title': f'ویرایش برند: {brand.name}', 'brand': brand})


@staff_required
def brand_delete_view(request, pk):
    brand = get_object_or_404(Brand, pk=pk)
    if request.method == "POST":
        name = brand.name
        brand.delete()
        AdminActionLog.objects.create(
            admin=request.user, action="Delete Brand",
            details=f"Deleted brand '{name}'"
        )
        # For modal-ajax deletion:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"success": True})
        # Fallback full redirect (if someone submits a normal form):
        messages.success(request, "برند حذف شد.")
        return redirect("admin_dashboard:admin_brands")

    # GET → full page confirm (your confirm_delete.html)
    return render(request, 'admin_dashboard/brands/confirm_delete.html', {'brand': brand})


# --- PRODUCT CRUD ---
@staff_required
def api_get_product_data(request, product_id):
    """
    Fetches a single product's data by ID and returns it as JSON.
    """
    try:
        product = Product.objects.get(pk=product_id)

        # Corrected: Handle the features field
        features_data = {}  # Default to an empty dict
        if isinstance(product.features, dict):
            features_data = product.features
        elif isinstance(product.features, str):
            try:
                features_data = json.loads(product.features)
            except json.JSONDecodeError:
                pass

        # Corrected: Handle the related products field
        # Ensure rel_products is always a list before trying to iterate over it
        rel_products_list = []
        if isinstance(product.rel_products, list):
            rel_products_list = product.rel_products
        elif isinstance(product.rel_products, int):
            rel_products_list = [product.rel_products]

        rel_products_data = [
            {"id": str(p.pk), "text": p.name or p.english_name or f"Product #{p.pk}"}
            for p in Product.objects.filter(pk__in=rel_products_list)
        ]

        # Build the full data dictionary
        data = {
            "name": product.name,
            "categories": [
                {"id": str(c.pk), "text": c.name or c.english_name or c.slug or f"Category #{c.pk}"}
                for c in product.categories.all()
            ],
            "rel_blogs": [
                {"id": str(b.pk), "text": b.name or b.english_name or f"Blog #{b.pk}"}
                for b in Blog.objects.filter(pk__in=product.rel_blogs) if isinstance(product.rel_blogs, list)
            ],
            "rel_news": [
                {"id": str(n.pk), "text": n.name or n.english_name or f"News #{n.pk}"}
                for n in News.objects.filter(pk__in=product.rel_news) if isinstance(product.rel_news, list)
            ],
            "rel_products": rel_products_data,
            "features": features_data
        }

        return JsonResponse(data)

    except Product.DoesNotExist:
        return JsonResponse({"error": "Product not found"}, status=404)
    except Exception as e:
        print(f"Error during API call for product {product_id}:", e)
        return JsonResponse({"error": str(e)}, status=500)


@staff_required
def api_search_categories(request):
    from categories.models import Category
    q = (request.GET.get("q") or "").strip()
    qs = Category.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(english_name__icontains=q) | Q(slug__icontains=q))
    qs = qs.order_by('name')[:50]
    data = [{"id": str(c.pk), "text": c.name or c.english_name or c.slug or f"Category #{c.pk}"} for c in qs]
    return JsonResponse({"results": data})


@staff_required
def api_search_blogs(request):
    q = (request.GET.get("q") or "").strip()
    qs = Blog.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(english_name__icontains=q))
    qs = qs.select_related("writer").order_by("-publish_time")[:20]
    data = [{"id": obj.pk, "text": obj.name or obj.english_name or f"Blog #{obj.pk}"} for obj in qs]
    return JsonResponse({"results": data})


@staff_required
def api_search_news(request):
    q = (request.GET.get("q") or "").strip()
    qs = News.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(english_name__icontains=q))
    qs = qs.select_related("writer").order_by("-publish_time")[:20]
    data = [{"id": obj.pk, "text": obj.name or obj.english_name or f"News #{obj.pk}"} for obj in qs]
    return JsonResponse({"results": data})


@staff_required
def api_search_products(request):
    q = (request.GET.get("q") or "").strip()
    qs = Product.objects.all()
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(english_name__icontains=q))
    qs = qs.select_related("brand").order_by("-created_at")[:20]

    def label(p):
        t = p.name or p.english_name or f"Product #{p.pk}"
        return f"{t} ({p.brand.name})" if getattr(p, "brand", None) else t

    data = [{"id": p.pk, "text": label(p)} for p in qs]
    return JsonResponse({"results": data})


@method_staff_required
class ProductListView(ListView):
    model = Product
    template_name = 'admin_dashboard/products/list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        q = self.request.GET.get('q')
        qs = Product.objects.select_related('brand').all().order_by('-created_at')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(english_name__icontains=q)
        return qs


def _save_extra_images(files):
    """Save uploaded images and return a list of their media URLs/paths."""
    saved = []
    for f in files:
        # store under products/<filename> (unique name is ensured by storage)
        path = default_storage.save(f"products/{f.name}", ContentFile(f.read()))
        # If you want absolute URL: settings.MEDIA_URL + path
        saved.append(f"{settings.MEDIA_URL}{path}".rstrip("/"))
    return saved


@staff_required
def product_create_view(request):
    if request.method == "POST":
        # normalize price (digits only) if present in POST
        if "price" in request.POST:
            request.POST = request.POST.copy()
            request.POST["price"] = request.POST["price"].replace(",", "")

        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            # ensure features is dict (JSONField)
            features = form.cleaned_data.get("features")
            if isinstance(features, str):
                try:
                    form.instance.features = json.loads(features or "{}")
                except Exception:
                    form.instance.features = {}

            product = form.save()

            # handle extra images
            extra_files = request.FILES.getlist("extra_images")
            if extra_files and hasattr(product, "images"):
                new_urls = _save_extra_images(extra_files)
                try:
                    current = list(product.images or [])
                except Exception:
                    current = []
                product.images = current + new_urls
                product.save(update_fields=["images"])

            AdminActionLog.objects.create(
                admin=request.user,
                action="Create Product",
                details=f"Product '{product.name}' created"
            )
            return redirect('admin_dashboard:admin_products')
    else:
        form = ProductForm()

    # currency unit for template label
    ctx = {'form': form, 'title': 'ایجاد محصول', 'CURRENCY_UNIT': getattr(settings, "CURRENCY_UNIT", "ریال")}
    return render(request, 'admin_dashboard/products/form.html', ctx)


@staff_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        if "price" in request.POST:
            request.POST = request.POST.copy()
            request.POST["price"] = request.POST["price"].replace(",", "")
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            features = form.cleaned_data.get("features")
            if isinstance(features, str):
                try:
                    form.instance.features = json.loads(features or "{}")
                except Exception:
                    form.instance.features = {}

            product = form.save()

            extra_files = request.FILES.getlist("extra_images")
            if extra_files and hasattr(product, "images"):
                new_urls = _save_extra_images(extra_files)
                try:
                    current = list(product.images or [])
                except Exception:
                    current = []
                product.images = current + new_urls
                product.save(update_fields=["images"])

            AdminActionLog.objects.create(
                admin=request.user,
                action="Update Product",
                details=f"Updated product '{product.name}'"
            )
            return redirect('admin_dashboard:admin_products')
    else:
        form = ProductForm(instance=product)

    ctx = {'form': form, 'title': f'ویرایش محصول: {product.name}',
           'CURRENCY_UNIT': getattr(settings, "CURRENCY_UNIT", "ریال")}
    return render(request, 'admin_dashboard/products/form.html', ctx)


@staff_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        name = product.name
        product.delete()
        AdminActionLog.objects.create(
            admin=request.user,
            action="Delete Product",
            details=f"Deleted product '{name}'"
        )
        # AJAX (modal) path:
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({'success': True})
        return redirect('admin_dashboard:admin_products')
    return render(request, 'admin_dashboard/products/confirm_delete.html', {'product': product})


# ---------------- Writers ----------------
@admin_required
def admin_writers_list(request):
    q = request.GET.get("q", "").strip()
    writers = Writer.objects.select_related("user").all().order_by("-id")
    if q:
        writers = writers.filter(user__phone_number__icontains=q) | writers.filter(
            first_name__icontains=q) | writers.filter(last_name__icontains=q) | writers.filter(email__icontains=q)
    paginator = Paginator(writers, 20)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "admin_dashboard/writers/list.html", {"page_obj": page_obj, "q": q})


@admin_required
@transaction.atomic
def admin_writers_create(request):
    if request.method == "POST":
        form = AdminCreateWriterForm(request.POST, request.FILES)
        if form.is_valid():
            # create user
            user = User.objects.create_user(
                phone_number=form.cleaned_data["phone_number"],
                password=form.cleaned_data["password"],
                role="writer",
                is_staff=True,  # allow panel login
            )
            # create writer profile
            writer = Writer.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                age=form.cleaned_data["age"],
                email=form.cleaned_data["email"],
                about_me=form.cleaned_data.get("about_me", ""),
                profile_image=form.cleaned_data.get("profile_image"),
            )
            # set permissions
            WriterPermission.objects.create(
                user=user,
                can_write_blogs=form.cleaned_data.get("can_write_blogs", False),
                can_write_news=form.cleaned_data.get("can_write_news", False),
            )
            messages.success(request, "نویسنده جدید ایجاد شد.")
            return redirect("admin_dashboard:admin_writers")
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")
    else:
        form = AdminCreateWriterForm()
    return render(request, "admin_dashboard/writers/create.html", {"form": form})


@admin_required
@transaction.atomic
def admin_writers_edit(request, pk):
    writer = get_object_or_404(Writer, pk=pk)
    perm = getattr(writer.user, "writer_permission", None)
    initial = {
        "first_name": writer.first_name,
        "last_name": writer.last_name,
        "age": writer.age,
        "email": writer.email,
        "about_me": writer.about_me,
        "can_write_blogs": perm.can_write_blogs if perm else False,
        "can_write_news": perm.can_write_news if perm else False,
    }
    if request.method == "POST":
        form = AdminUpdateWriterForm(request.POST, request.FILES)
        if form.is_valid():
            writer.first_name = form.cleaned_data["first_name"]
            writer.last_name = form.cleaned_data["last_name"]
            writer.age = form.cleaned_data["age"]
            writer.email = form.cleaned_data["email"]
            writer.about_me = form.cleaned_data.get("about_me", "")
            if form.cleaned_data.get("profile_image"):
                writer.profile_image = form.cleaned_data.get("profile_image")
            writer.save()
            # update permissions
            perm_obj, _ = WriterPermission.objects.get_or_create(user=writer.user)
            perm_obj.can_write_blogs = form.cleaned_data.get("can_write_blogs", False)
            perm_obj.can_write_news = form.cleaned_data.get("can_write_news", False)
            perm_obj.save()
            messages.success(request, "اطلاعات نویسنده به‌روزرسانی شد.")
            return redirect("admin_dashboard:admin_writers")
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")
    else:
        form = AdminUpdateWriterForm(initial=initial)
    return render(request, "admin_dashboard/writers/edit.html", {"form": form, "writer": writer})


@admin_required
@transaction.atomic
def admin_writers_delete(request, pk):
    writer = get_object_or_404(Writer, pk=pk)
    if request.method == "POST":
        # deleting the user cascades to Writer (OneToOne)
        writer.user.delete()
        messages.success(request, "نویسنده حذف شد.")
        return redirect("admin_dashboard:admin_writers")
    return render(request, "admin_dashboard/writers/delete.html", {"writer": writer})


# ---------------- Sellers ----------------
@admin_required
def admin_sellers_list(request):
    q = request.GET.get("q", "").strip()
    sellers = Seller.objects.select_related("user").all().order_by("-id")
    if q:
        sellers = sellers.filter(user__phone_number__icontains=q) | sellers.filter(
            first_name__icontains=q) | sellers.filter(last_name__icontains=q) | sellers.filter(
            email__icontains=q) | sellers.filter(business_name__icontains=q)
    paginator = Paginator(sellers, 20)
    page = request.GET.get("page")
    page_obj = paginator.get_page(page)
    return render(request, "admin_dashboard/sellers/list.html", {"page_obj": page_obj, "q": q})


@admin_required
@transaction.atomic
def admin_sellers_create(request):
    if request.method == "POST":
        form = AdminCreateSellerForm(request.POST, request.FILES)
        if form.is_valid():
            user = User.objects.create_user(
                phone_number=form.cleaned_data["phone_number"],
                password=form.cleaned_data["password"],
                role="seller",
                is_staff=True,
            )
            seller = Seller.objects.create(
                user=user,
                first_name=form.cleaned_data["first_name"],
                last_name=form.cleaned_data["last_name"],
                age=form.cleaned_data["age"],
                email=form.cleaned_data["email"],
                about_us=form.cleaned_data.get("about_us", ""),
                profile_image=form.cleaned_data.get("profile_image"),
                address=form.cleaned_data["address"],
                location=form.cleaned_data.get("location"),
                business_name=form.cleaned_data["business_name"],
                business_code=form.cleaned_data["business_code"],
            )
            messages.success(request, "فروشنده جدید ایجاد شد.")
            return redirect("admin_dashboard:admin_sellers")
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")
    else:
        form = AdminCreateSellerForm()
    return render(request, "admin_dashboard/sellers/create.html", {"form": form})


@admin_required
@transaction.atomic
def admin_sellers_edit(request, pk):
    seller = get_object_or_404(Seller, pk=pk)
    initial = {
        "first_name": seller.first_name,
        "last_name": seller.last_name,
        "age": seller.age,
        "email": seller.email,
        "about_us": seller.about_us,
        "address": seller.address,
        "location": seller.location,
        "business_name": seller.business_name,
        "business_code": seller.business_code,
    }
    if request.method == "POST":
        form = AdminUpdateSellerForm(request.POST, request.FILES)
        if form.is_valid():
            seller.first_name = form.cleaned_data["first_name"]
            seller.last_name = form.cleaned_data["last_name"]
            seller.age = form.cleaned_data["age"]
            seller.email = form.cleaned_data["email"]
            seller.about_us = form.cleaned_data.get("about_us", "")
            if form.cleaned_data.get("profile_image"):
                seller.profile_image = form.cleaned_data.get("profile_image")
            seller.address = form.cleaned_data["address"]
            seller.location = form.cleaned_data.get("location")
            seller.business_name = form.cleaned_data["business_name"]
            seller.business_code = form.cleaned_data["business_code"]
            seller.save()
            messages.success(request, "اطلاعات فروشنده به‌روزرسانی شد.")
            return redirect("admin_dashboard:admin_sellers")
        else:
            messages.error(request, "لطفاً خطاهای فرم را بررسی کنید.")
    else:
        form = AdminUpdateSellerForm(initial=initial)
    return render(request, "admin_dashboard/sellers/edit.html", {"form": form, "seller": seller})


@admin_required
@transaction.atomic
def admin_sellers_delete(request, pk):
    seller = get_object_or_404(Seller, pk=pk)
    if request.method == "POST":
        seller.user.delete()
        messages.success(request, "فروشنده حذف شد.")
        return redirect("admin_dashboard:admin_sellers")
    return render(request, "admin_dashboard/sellers/delete.html", {"seller": seller})


# ---- TAGS ----
@admin_required
def admin_tag_list(request):
    q = request.GET.get("q", "")
    qs = Tag.objects.all().annotate(
        blog_count=Count("blogs", distinct=True),
        news_count=Count("news_items", distinct=True),
    )
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(slug__icontains=q))
    qs = qs.order_by("name")
    paginator = Paginator(qs, 20)
    page_obj = paginator.get_page(request.GET.get("page"))
    # usage_count را محاسبه کنیم
    tags = []
    for t in page_obj.object_list:
        t.usage_count = (getattr(t, "blog_count", 0) or 0) + (getattr(t, "news_count", 0) or 0)
        tags.append(t)
    return render(request, "admin_dashboard/tags/list.html", {"tags": tags, "page_obj": page_obj})


@admin_required
def admin_tag_create(request):
    if request.method == "POST":
        form = TagForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "برچسب با موفقیت ایجاد شد.")
            return redirect("admin_dashboard:admin_tags")
    else:
        form = TagForm()
    return render(request, "admin_dashboard/tags/create.html", {"form": form})


@admin_required
def admin_tag_edit(request, pk):
    obj = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        form = TagForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            messages.success(request, "برچسب با موفقیت به‌روزرسانی شد.")
            return redirect("admin_dashboard:admin_tags")
    else:
        form = TagForm(instance=obj)
    return render(request, "admin_dashboard/tags/edit.html", {"form": form, "obj": obj})


@admin_required
def admin_tag_delete(request, pk):
    obj = get_object_or_404(Tag, pk=pk)
    if request.method == "POST":
        obj.delete()
        messages.success(request, "برچسب حذف شد.")
        return redirect("admin_dashboard:admin_tags")
    return render(request, "admin_dashboard/tags/delete.html", {"obj": obj})
