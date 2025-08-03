from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from comments.models import Comment
from blogs.models.blog import Blog
from news.models.news import News
from django.contrib.contenttypes.models import ContentType


@login_required
def blog_comments_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, writer=request.user)
    comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Blog),
        object_id=blog.id
    ).order_by('-created_at')

    return render(request, "blog_comments.html", {
        "blog": blog,
        "comments": comments
    })


@login_required
def news_comments_view(request, news_id):
    news = get_object_or_404(News, id=news_id, writer=request.user)
    comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(News),
        object_id=news.id
    ).order_by('-created_at')

    return render(request, "news_comments.html", {
        "news": news,
        "comments": comments
    })
