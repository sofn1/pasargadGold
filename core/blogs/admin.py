from .models.blog import Blog
from django.contrib import admin


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    # Keep it minimal/safe — adjust fields if your model uses different names.
    list_display = ("id", "title")
    search_fields = ("title",)
    list_filter = tuple()


# ⬇️ Tag integrations
filter_horizontal = getattr(BlogAdmin, "filter_horizontal", tuple()) + ("tags",)
search_fields = getattr(BlogAdmin, "search_fields", tuple()) + ("tags__name",)
list_filter = getattr(BlogAdmin, "list_filter", tuple()) + ("tags",)
