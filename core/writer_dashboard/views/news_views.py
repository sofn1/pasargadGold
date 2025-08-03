from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from news.models.news import News
from writer_dashboard.forms import WriterNewsForm as NewsForm


@method_decorator(login_required, name='dispatch')
class NewsListView(ListView):
    model = News
    template_name = "news/list.html"
    context_object_name = 'news_list'

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)


@method_decorator(login_required, name='dispatch')
class NewsCreateView(CreateView):
    model = News
    form_class = NewsForm
    template_name = "news/create.html"
    success_url = reverse_lazy("writer:news_list")

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class NewsUpdateView(UpdateView):
    model = News
    form_class = NewsForm
    template_name = "news/edit.html"
    success_url = reverse_lazy("writer:news_list")

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)


@method_decorator(login_required, name='dispatch')
class NewsDeleteView(DeleteView):
    model = News
    template_name = "news/delete.html"
    success_url = reverse_lazy("writer:news_list")

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)
