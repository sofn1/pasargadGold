from .models.product import Product
from rest_framework import serializers
from .mongo_service.category_service import ProductCategoryService


# --- MongoDB category ---
class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategoryService
        fields = '__all__'


# --- PostgreSQL product ---
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
