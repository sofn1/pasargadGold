# products/views.py
from django.views.generic import TemplateView, ListView, DetailView
from django.http import Http404
from django.db.models import Q, Prefetch
from .models.product import Product
from categories.services import ProductCategoryService


def _map_category_doc(doc):
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "english_name": doc.get("englishName"),
        "sub_categories": [str(x) for x in doc.get("subCategories", [])],
        "image": doc.get("image"),
        "slug": doc.get("slug"),
        "parent_id": str(doc.get("parent_id")) if doc.get("parent_id") else None,
    }


# ===== Categories (Mongo) =====
class ProductCategoryListPage(TemplateView):
    template_name = "products/category_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = ProductCategoryService()
        raw = service.get_all_categories()
        ctx["categories"] = [_map_category_doc(c) for c in raw]
        return ctx


class ProductCategoryDetailPage(TemplateView):
    template_name = "products/category_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category_id = kwargs.get("pk")
        service = ProductCategoryService()
        doc = service.get_category(category_id)
        category = _map_category_doc(doc)
        if not category:
            raise Http404("Category not found")

        ctx["category"] = category
        ctx["products"] = (
            Product.objects.select_related("brand")
            .filter(is_active=True, category_id=category_id)
            .order_by("-created_at")
        )
        return ctx


# ===== Products (Postgres) =====
class ProductListPage(ListView):
    template_name = "products/product_list.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        qs = (
            Product.objects.select_related("brand")
            .filter(is_active=True)
            .order_by("-created_at")
        )
        # Optional filters
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category_id=category)

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(english_name__icontains=q) |
                Q(short_description__icontains=q) |
                Q(description__icontains=q)
            )

        brand = self.request.GET.get("brand")
        if brand:
            qs = qs.filter(brand__name__iexact=brand)

        featured = self.request.GET.get("featured")
        if featured in {"1", "true", "True"}:
            qs = qs.filter(featured=True)

        return qs


class ProductDetailPage(DetailView):
    template_name = "products/product_detail.html"
    model = Product
    context_object_name = "product"

    def get_queryset(self):
        return Product.objects.select_related("brand").filter(is_active=True)


class FeaturedProductsPage(ListView):
    template_name = "products/featured.html"
    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        return (
            Product.objects.select_related("brand")
            .filter(is_active=True, featured=True)
            .order_by("-created_at")
        )
