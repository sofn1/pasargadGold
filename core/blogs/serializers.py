from .models.blog import Blog
from rest_framework import serializers
from .mongo_service.category_service import BlogCategoryService


class BlogCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogCategoryService
        fields = '__all__'


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
