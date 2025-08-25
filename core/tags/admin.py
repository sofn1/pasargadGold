from django.contrib import admin
from django.db.models import Count
from .models import Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "color", "usage_count")
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    list_per_page = 25

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # این نام‌های related_name را در بخش ادغام با Blog/News تعریف می‌کنیم
        return qs.annotate(
            blog_count=Count("blogs", distinct=True),
            news_count=Count("news_items", distinct=True),
        )

    @admin.display(description="تعداد استفاده")
    def usage_count(self, obj):
        return (getattr(obj, "blog_count", 0) or 0) + (getattr(obj, "news_count", 0) or 0)
