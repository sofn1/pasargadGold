# news/views.py
from .models.news import News
from django.db.models import Q
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from .mongo_service.category_service import NewsCategoryService
from django.views.generic import TemplateView, ListView, DetailView


def _map_category_doc(doc):
    """Normalize a Mongo category document for templates."""
    if not doc:
        return None
    return {
        "id": str(doc.get("_id")),
        "name": doc.get("name"),
        "english_name": doc.get("englishName"),
        "sub_categories": [str(x) for x in doc.get("subCategories", [])],
    }


class NewsCategoryListPage(LoginRequiredMixin, TemplateView):
    template_name = "news/category_list.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        service = NewsCategoryService()
        raw = service.get_all_categories()  # list of dicts with _id
        ctx["categories"] = [_map_category_doc(c) for c in raw]
        return ctx


class NewsCategoryDetailPage(LoginRequiredMixin, TemplateView):
    template_name = "news/category_detail.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        category_id = kwargs.get("pk")
        service = NewsCategoryService()
        doc = service.get_category(category_id)
        category = _map_category_doc(doc)
        if not category:
            raise Http404("Category not found")

        ctx["category"] = category
        ctx["news_list"] = (
            News.objects.filter(category_id=category_id)
            .order_by("-publish_time")
        )
        return ctx


class NewsListPage(LoginRequiredMixin, ListView):
    template_name = "news/news_list.html"
    context_object_name = "news_list"
    paginate_by = 10

    def get_queryset(self):
        qs = News.objects.all().order_by("-publish_time")
        category = self.request.GET.get("category")
        if category:
            qs = qs.filter(category_id=category)

        q = self.request.GET.get("q")
        if q:
            qs = qs.filter(
                Q(name__icontains=q) |
                Q(english_name__icontains=q) |
                Q(short_description__icontains=q)
            )
        return qs


class NewsDetailPage(LoginRequiredMixin, DetailView):
    template_name = "news/news_detail.html"
    model = News
    context_object_name = "news"
