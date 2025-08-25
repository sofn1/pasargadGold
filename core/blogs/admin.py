from .models.blog import Blog
from django.contrib import admin
from django.core.exceptions import FieldDoesNotExist


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Always valid: show ID and a computed title/name
    list_display = ("id", "display_title")
    list_filter = tuple()  # we'll extend with "tags" below via getattr

    # search_fields is provided via get_search_fields to avoid system check errors

    @admin.display(description="عنوان")
    def display_title(self, obj):
        # Prefer common fields; otherwise fall back to __str__
        return getattr(obj, "title", None) or getattr(obj, "name", None) or str(obj)

    def get_search_fields(self, request):
        fields = []
        for f in ("title", "name", "slug"):
            try:
                self.model._meta.get_field(f)
                fields.append(f)
            except FieldDoesNotExist:
                pass
        # Add tag name search (works after you added M2M tags)
        fields.append("tags__name")
        return tuple(fields)


# ⬇️ Tag integrations (safe even if previously empty)
filter_horizontal = getattr(BlogAdmin, "filter_horizontal", tuple()) + ("tags",)
search_fields = getattr(BlogAdmin, "get_search_fields", None)  # handled via method above
list_filter = getattr(BlogAdmin, "list_filter", tuple()) + ("tags",)
