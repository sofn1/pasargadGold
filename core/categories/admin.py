from django.contrib import admin
from django.utils.html import format_html
from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("thumb", "name", "english_name", "slug", "parent", "is_active")
    list_filter = ("is_active",)
    search_fields = ("name", "english_name", "slug")
    autocomplete_fields = ("parent",)
    prepopulated_fields = {"slug": ("english_name",)}  # optional

    def thumb(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:32px;width:32px;object-fit:cover;border-radius:6px;" />', obj.image.url)
        return "-"
    thumb.short_description = "Img"
