# blogs/views.py
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, ListView, DetailView
from django.shortcuts import get_object_or_404
from .models.blog import Blog
from .mongo_service.category_service import BlogCategoryService


# ===== Categories (Mongo) =====
class BlogCategoryListPage(LoginRequiredMixin, TemplateView):
    template_name = "blogs/category_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = BlogCategoryService()
        ctx["categories"] = service.get_all_categories()  # list[dict]
        return ctx


class BlogCategoryDetailPage(LoginRequiredMixin, TemplateView):
    template_name = "blogs/category_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category_id = kwargs.get("pk")
        service = BlogCategoryService()
        category = service.get_category(category_id)
        if not category:
            # Keep consistent behavior with 404 if not found
            # Since we don't have a Django model, we emulate 404 by raising manually.
            from django.http import Http404
            raise Http404("Category not found")

        ctx["category"] = category
        # Blogs linked to this Mongo category (Blog.category_id is a string)
        ctx["blogs"] = Blog.objects.filter(category_id=category_id).order_by("-publish_time")
        return ctx


# ===== Blogs (PostgreSQL model) =====
class BlogListPage(LoginRequiredMixin, ListView):
    template_name = "blogs/blog_list.html"
    context_object_name = "blogs"
    paginate_by = 10

    def get_queryset(self):
        qs = Blog.objects.all().order_by("-publish_time")
        # Optional filter by category via ?category=<mongo_id>
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category_id=category)
        # Optional search by title/name/short_description (?q=...)
        q = self.request.GET.get("q")
        if q:
            from django.db.models import Q
            qs = qs.filter(
                Q(name__icontains=q) | Q(english_name__icontains=q) | Q(short_description__icontains=q)
            )
        return qs


class BlogDetailPage(LoginRequiredMixin, DetailView):
    template_name = "blogs/blog_detail.html"
    model = Blog
    context_object_name = "blog"
