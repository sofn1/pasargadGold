# heroes/views.py
from django.views.generic import ListView
from .models import Hero


class HeroListPage(ListView):
    model = Hero
    template_name = "heroes/list.html"   # templates/heroes/list.html
    context_object_name = "heroes"

    def get_queryset(self):
        # Only show active heroes, newest first (adjust if you add priority field later)
        return Hero.objects.filter(is_active=True).order_by("-id")
