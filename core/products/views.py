from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from .models.product import Product
from .serializers import ProductSerializer, ProductCategorySerializer
from .mongo_service.category_service import ProductCategoryService


# ========== Product Category Views (MongoDB) ==========

class ProductCategoryListCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        service = ProductCategoryService()
        categories = service.get_all_categories()
        return Response(categories)

    def post(self, request):
        service = ProductCategoryService()
        name = request.data.get("name")
        english_name = request.data.get("english_name")
        parent_id = request.data.get("parent_id")

        if not name or not english_name:
            return Response({"error": "name and english_name are required"}, status=status.HTTP_400_BAD_REQUEST)

        category_id = service.create_category(name, english_name, parent_id)
        return Response({"id": category_id}, status=status.HTTP_201_CREATED)


class ProductCategoryDetailView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        service = ProductCategoryService()
        category = service.get_category(pk)
        if category:
            return Response(category)
        return Response({"error": "Not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        service = ProductCategoryService()
        name = request.data.get("name")
        english_name = request.data.get("english_name")
        service.update_category(pk, name, english_name)
        return Response({"message": "Updated"})

    def delete(self, request, pk):
        service = ProductCategoryService()
        service.delete_category(pk)
        return Response({"message": "Deleted"}, status=status.HTTP_204_NO_CONTENT)


# ========== Product Views (PostgreSQL) ==========
class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]


class FeaturedProductsView(generics.ListAPIView):
    queryset = Product.objects.filter(featured=True)
    serializer_class = ProductSerializer
    permission_classes = [permissions.AllowAny]


