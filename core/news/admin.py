from .models.news import News
from django.contrib import admin


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # Keep it minimal/safe — adjust fields if your model uses different names.
    list_display = ("id", "title")
    search_fields = ("title",)
    list_filter = tuple()


# ⬇️ Tag integrations
filter_horizontal = getattr(NewsAdmin, "filter_horizontal", tuple()) + ("tags",)
search_fields = getattr(NewsAdmin, "search_fields", tuple()) + ("tags__name",)
list_filter = getattr(NewsAdmin, "list_filter", tuple()) + ("tags",)
