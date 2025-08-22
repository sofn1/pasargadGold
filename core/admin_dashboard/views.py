# admin_dashboard/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Sum
from django.http import JsonResponse
from django.views import View
from django.views.generic import ListView, DetailView
from django.utils.decorators import method_decorator
from django.db.models.deletion import ProtectedError

from heroes.models import Hero
from datetime import timedelta
from django.urls import reverse
from accounts.models import User
from banners.models import Banner
from news.models.news import News
from blogs.models.blog import Blog
from django.contrib import messages
from comments.models import Comment
from logs.models import AdminActionLog
from categories.models import Category
from products.models.brand import Brand
from orders.models import Order, CartItem
from payments.models import FailedPayment
from products.models.product import Product
from products.mongo_service.category_service import ProductCategoryService
from .forms import BlogForm, NewsForm, BannerForm, HeroForm, BrandForm, ProductForm, CategoryForm, CategoryCreateForm

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


class ProductListView(ListView):
    model = Product
    template_name = 'admin_dashboard/products/products.html'
    context_object_name = 'products'
    paginate_by = 20

    def get_queryset(self):
        qs = Product.objects.select_related('brand').all().order_by('-created_at')
        q = self.request.GET.get('q')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(english_name__icontains=q)
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
            'revenue': float(Order.objects.filter(status='paid').aggregate(Sum('total_price'))['total_price__sum'] or 0),
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

def get_category_service():
    """Helper to instantiate the service."""
    return ProductCategoryService()


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
        q = self.request.GET.get('q')
        qs = Blog.objects.select_related('writer').all().order_by('-publish_time')
        if q:
            qs = qs.filter(name__icontains=q) | qs.filter(english_name__icontains=q)
        return qs
    

@staff_required
def blog_create_view(request):
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Create Blog",
                details=f"Created blog '{blog.name}' (ID: {blog.id})"
            )
            return redirect('admin_dashboard:blogs')
    else:
        form = BlogForm()
    return render(request, 'admin_dashboard/blogs/form.html', {'form': form, 'title': 'Create Blog'})


@staff_required
def blog_edit_view(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    if request.method == "POST":
        form = BlogForm(request.POST, request.FILES, instance=blog)
        if form.is_valid():
            blog = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Update Blog",
                details=f"Updated blog '{blog.name}' (ID: {blog.id})"
            )
            return redirect('admin_dashboard:blogs')
    else:
        form = BlogForm(instance=blog)
    return render(request, 'admin_dashboard/blogs/form.html', {'form': form, 'title': f'Edit Blog: {blog.name}', 'blog': blog})


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
    return render(request, 'admin_dashboard/news/form.html', {'form': form, 'title': f'Edit News: {news.name}', 'news': news})


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
                details=f"Hero '{hero.title}' created"
            )
            return redirect('admin_dashboard:heroes')
    else:
        form = HeroForm()
    return render(request, 'admin_dashboard/heroes/form.html', {'form': form, 'title': 'Create Hero'})


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
                details=f"Updated hero '{hero.title}'"
            )
            return redirect('admin_dashboard:heroes')
    else:
        form = HeroForm(instance=hero)
    return render(request, 'admin_dashboard/heroes/form.html', {'form': form, 'title': f'Edit Hero: {hero.title}'})


@staff_required
def hero_delete_view(request, pk):
    hero = get_object_or_404(Hero, pk=pk)
    if request.method == "POST":
        title = hero.title
        hero.delete()
        AdminActionLog.objects.create(
            admin=request.user,
            action="Delete Hero",
            details=f"Deleted hero '{title}'"
        )
        return JsonResponse({'success': True})
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


@staff_required
def product_create_view(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Create Product",
                details=f"Product '{product.name}' created"
            )
            return redirect('admin_dashboard:products')
    else:
        form = ProductForm()
    return render(request, 'admin_dashboard/products/form.html', {'form': form, 'title': 'Create Product'})


@staff_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            product = form.save()
            AdminActionLog.objects.create(
                admin=request.user,
                action="Update Product",
                details=f"Updated product '{product.name}'"
            )
            return redirect('admin_dashboard:products')
    else:
        form = ProductForm(instance=product)
    return render(request, 'admin_dashboard/products/form.html', {'form': form, 'title': f'Edit Product: {product.name}'})


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
        return JsonResponse({'success': True})
    return render(request, 'admin_dashboard/products/confirm_delete.html', {'product': product})
