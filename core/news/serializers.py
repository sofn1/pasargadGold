from .models.news import News
from rest_framework import serializers
from .mongo_service.category_service import NewsCategoryService


class NewsCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NewsCategoryService
        fields = '__all__'


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
