# core/writer_dashboard/serializers.py
from rest_framework import serializers
from blogs.models.blog import Blog
from news.models.news import News
from comments.models import Comment


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = '__all__'
        read_only_fields = ['writer', 'publishTime', 'views']


class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        read_only_fields = ['writer', 'publishTime', 'views']


class RecursiveCommentSerializer(serializers.Serializer):
    def to_representation(self, value):
        return CommentSerializer(value, context=self.context).data


class CommentSerializer(serializers.ModelSerializer):
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ['id', 'user', 'content', 'created_at', 'replies']

    def get_replies(self, obj):
        child_comments = Comment.objects.filter(parent=obj).order_by('created_at')
        return RecursiveCommentSerializer(child_comments, many=True, context=self.context).data
