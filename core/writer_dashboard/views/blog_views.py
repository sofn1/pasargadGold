from blogs.models.blog import Blog
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from writer_dashboard.forms import WriterBlogForm as BlogForm
from django.views.generic import ListView, CreateView, UpdateView, DeleteView


@method_decorator(login_required, name='dispatch')
class BlogListView(ListView):
    model = Blog
    template_name = "writer_dashboard/blogs/list.html"
    context_object_name = 'blogs'

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user).order_by("-publish_time")


@method_decorator(login_required, name='dispatch')
class BlogCreateView(CreateView):
    model = Blog
    form_class = BlogForm
    template_name = "writer_dashboard/blogs/create.html"
    success_url = reverse_lazy("writer:blog_list")

    def form_valid(self, form):
        form.instance.writer = self.request.user
        form.instance.writer_name = self.request.user.get_full_name() or self.request.user.username
        # Optional: set profile URL if you have it on user
        # form.instance.writer_profile = getattr(self.request.user, "profile_url", "")
        return super().form_valid(form)


@method_decorator(login_required, name='dispatch')
class BlogUpdateView(UpdateView):
    model = Blog
    form_class = BlogForm
    template_name = "writer_dashboard/blogs/edit.html"
    success_url = reverse_lazy("writer:blog_list")

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)


@method_decorator(login_required, name='dispatch')
class BlogDeleteView(DeleteView):
    model = Blog
    template_name = "writer_dashboard/blogs/delete.html"
    success_url = reverse_lazy("writer:blog_list")

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)
