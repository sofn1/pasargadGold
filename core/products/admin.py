from .models.brand import Brand
from django.contrib import admin
from .models.product import Product
from .forms import ProductAdminForm


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    list_display = ('name', 'price', 'is_active', 'brand')
    list_filter = ('brand', 'is_active')
    search_fields = ('name',)


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name',)
