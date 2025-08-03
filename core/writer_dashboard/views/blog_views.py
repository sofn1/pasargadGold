from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from blogs.models.blog import Blog
from writer_dashboard.forms import WriterBlogForm as BlogForm


@method_decorator(login_required, name='dispatch')
class BlogListView(ListView):
    model = Blog
    template_name = "blogs/list.html"
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)


@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/create.html"
    success_url = reverse_lazy("writer:blog_list")

    def form_valid(self, form):
        form.instance.writer = self.request.user
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "blogs/edit.html"
    success_url = reverse_lazy("writer:blog_list")

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)


@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "blogs/delete.html"
    success_url = reverse_lazy("writer:blog_list")

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)
