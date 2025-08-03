from django.contrib import admin
from .models import Banner


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'position', 'priority', 'is_active')
    list_filter = ('position', 'is_active')
    search_fields = ('title',)
