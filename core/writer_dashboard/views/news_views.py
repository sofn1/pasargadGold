from news.models.news import News
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from writer_dashboard.forms import WriterNewsForm as NewsForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


@method_decorator(login_required, name='dispatch')
class NewsListView(ListView):
    model = News
    template_name = "writer_dashboard/news/list.html"
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user).order_by("-publish_time")


@method_decorator(login_required, name='dispatch')
class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = "writer_dashboard/news/create.html"
    success_url = reverse_lazy("writer:news_list")

    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.writer_name = self.request.user.get_full_name() or self.request.user.username
        # form.instance.writer_profile = getattr(self.request.user, "profile_url", "")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = "writer_dashboard/news/edit.html"
    success_url = reverse_lazy("writer:news_list")

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)


@method_decorator(login_required, name='dispatch')
class NewsDeleteView(DeleteView):
    model = News
    template_name = "writer_dashboard/news/delete.html"
    success_url = reverse_lazy("writer:news_list")

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)
