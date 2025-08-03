# banners/views.py
from rest_framework.generics import ListAPIView
from .models import Banner
from .serializers import BannerSerializer


class BannerListView(ListAPIView):
    queryset = Banner.objects.all()
    serializer_class = BannerSerializer
