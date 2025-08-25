from .models.news import News
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("id", "display_title")
    list_filter = tuple()

    @admin.display(description="عنوان")
    def display_title(self, obj):
        return getattr(obj, "title", None) or getattr(obj, "name", None) or str(obj)

    def get_search_fields(self, request):
        fields = []
        for f in ("title", "name", "slug"):
            try:
                self.model._meta.get_field(f)
                fields.append(f)
            except FieldDoesNotExist:
                pass
        fields.append("tags__name")
        return tuple(fields)


# ⬇️ Tag integrations
filter_horizontal = getattr(NewsAdmin, "filter_horizontal", tuple()) + ("tags",)
search_fields = getattr(NewsAdmin, "get_search_fields", None)  # provided via method
list_filter = getattr(NewsAdmin, "list_filter", tuple()) + ("tags",)
