# heroes/views.py
from rest_framework.generics import ListAPIView
from .models import Hero
from .serializers import HeroSerializer


class HeroListView(ListAPIView):
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
