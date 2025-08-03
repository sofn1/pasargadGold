from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models.blog import Blog
from .serializers import BlogSerializer, BlogCategorySerializer
from .mongo_service.category_service import BlogCategoryService


# ========== Blog Category Views ==========
class BlogCategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service = BlogCategoryService()
        categories = service.get_all_categories()
        return Response(categories)

    def post(self, request):
        service = BlogCategoryService()
        name = request.data.get("name")
        english_name = request.data.get("english_name")
        parent_id = request.data.get("parent_id")

        if not name or not english_name:
            return Response({"error": "name and english_name are required"}, status=status.HTTP_400_BAD_REQUEST)

        category_id = service.create_category(name, english_name, parent_id)
        return Response({"id": category_id}, status=status.HTTP_201_CREATED)


class BlogCategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        service = BlogCategoryService()
        category = service.get_category(pk)
        if category:
            return Response(category)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        service = BlogCategoryService()
        name = request.data.get("name")
        english_name = request.data.get("english_name")
        service.update_category(pk, name, english_name)
        return Response({"message": "Updated"})

    def delete(self, request, pk):
        service = BlogCategoryService()
        service.delete_category(pk)
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


# ========== Blog Views ==========
class BlogListCreateView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [permissions.IsAuthenticated]
