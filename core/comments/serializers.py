from rest_framework import serializers
from .models import Comment
from accounts.serializers.user import UserSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class RecursiveCommentSerializer(serializers.Serializer):
    def to_representation(self, value):
        max_depth = self.context.get("max_depth", 2)
        current_depth = self.context.get("depth", 0)

        if current_depth >= max_depth:
            return []  # or None

        serializer = CommentDetailSerializer(
            value,
            context={**self.context, "depth": current_depth + 1}
        )
        return serializer.data


class CommentDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    replies = RecursiveCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'replies']


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['content_type', 'object_id', 'content', 'parent']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    replies = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id',
            'user',
            'content',
            'created_at',
            'updated_at',
            'parent',
            'replies',
            'likes_count',
            'is_liked',
            'edited',
            'status',
        ]

    def get_user(self, obj):
        return {
            "id": obj.user.id,
            "username": obj.user.username,
            "profile_image": getattr(obj.user, 'profile_image', None)
        }

    def get_replies(self, obj):
        if obj.children.exists():
            return CommentSerializer(obj.children.all(), many=True, context=self.context).data
        return []

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_is_liked(self, obj):
        user = self.context.get('request').user
        return user.is_authenticated and obj.likes.filter(id=user.id).exists()
