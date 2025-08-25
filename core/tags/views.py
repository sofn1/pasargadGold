from django.db.models import Count, Q
from django.http import JsonResponse
from rest_framework import generics, permissions
from .models import Tag
from .serializers import TagSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    queryset = Tag.objects.all().annotate(
        blog_count=Count("blogs", distinct=True),
        news_count=Count("news_items", distinct=True),
    )
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.query_params.get("q")
        if q:
            qs = qs.filter(Q(name__icontains=q) | Q(slug__icontains=q))
        return qs.order_by("name")

    def list(self, request, *args, **kwargs):
        # اگر select2 می‌خواهید، از /api/tags/select2/ استفاده کنید (پایین)
        return super().list(request, *args, **kwargs)


class TagRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


def tag_select2(request):
    """
    خروجی سبک Select2: [{id, text, color}]
    پارامترها: ?q=term&limit=20
    """
    q = request.GET.get("q", "")
    limit = int(request.GET.get("limit", "20") or 20)
    qs = (
        Tag.objects
        .filter(Q(name__icontains=q) | Q(slug__icontains=q)) if q else Tag.objects.all()
    )
    qs = qs.order_by("name")[:max(1, min(limit, 100))]
    data = [{"id": t.id, "text": t.name, "color": t.color or ""} for t in qs]
    return JsonResponse({"results": data})
