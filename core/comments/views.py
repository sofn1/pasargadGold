import re
from .models import Comment
from .models import CommentLike
from accounts.models import User
from .permissions import IsOwnerOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions
from django.contrib.contenttypes.models import ContentType
from .serializers import CommentDetailSerializer, CommentCreateSerializer


class CommentUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOnly]


def extract_mentions(content):
    return re.findall(r'@(\w+)', content)


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        comment = serializer.save(user=self.request.user)

        # Detect mentions
        mentioned_usernames = extract_mentions(comment.content)
        mentioned_users = User.objects.filter(phone_number__in=mentioned_usernames)
        comment.mentions.set(mentioned_users)

        # Notify them
        for user in mentioned_users:
            print(f"📣 Notify {user.phone_number}: You were mentioned in a comment.")


class CommentListView(generics.ListAPIView):
    serializer_class = CommentDetailSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        model = self.kwargs['model']  # product/blog/news
        object_id = self.kwargs['object_id']

        model_class = {
            'product': 'products.product',
            'blog': 'blogs.blog',
            'news': 'news.news',
        }.get(model.lower())

        if not model_class:
            return Comment.objects.none()

        content_type = ContentType.objects.get(model=model_class.split(".")[1])
        return Comment.objects.filter(content_type=content_type, object_id=object_id, parent=None)


class ToggleLikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id):
        user = request.user
        try:
            comment = Comment.objects.get(pk=comment_id)
            like, created = CommentLike.objects.get_or_create(user=user, comment=comment)
            if not created:
                like.delete()
                return Response({"detail": "Unliked"}, status=200)
            return Response({"detail": "Liked"}, status=201)
        except Comment.DoesNotExist:
            return Response({"detail": "Comment not found"}, status=404)
