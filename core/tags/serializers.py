from rest_framework import serializers
from .models import Tag


class TagSerializer(serializers.ModelSerializer):
    usage_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Tag
        fields = ["id", "name", "slug", "color", "description", "usage_count", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "usage_count"]
