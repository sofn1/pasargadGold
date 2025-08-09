# banners/views.py
from django.views.generic import ListView
from .models import Banner


class BannerListPage(ListView):
    model = Banner
    template_name = "banners/list.html"   # templates/banners/list.html
    context_object_name = "banners"

    def get_queryset(self):
        # Show only active banners, ordered by priority (from model Meta)
        return Banner.objects.filter(is_active=True)
