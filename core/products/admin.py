from django.contrib import admin
from .models.product import Product
from .models.brand import Brand


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'is_active', 'brand')
    list_filter = ('brand', 'is_active')
    search_fields = ('name',)
