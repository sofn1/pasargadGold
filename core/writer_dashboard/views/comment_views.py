from news.models.news import News
from blogs.models.blog import Blog
from django.contrib import messages
from comments.models import Comment
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import render, get_object_or_404, redirect


@login_required
def blog_comments_view(request, blog_id):
    blog = get_object_or_404(Blog, id=blog_id, writer=request.user)
    comments = Comment.objects.filter(
        content_type=ContentType.objects.get_for_model(Blog),
        object_id=blog.id
    ).order_by('-created_at')

    return render(request, "writer_dashboard/blogs/blog_comments.html", {
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

    return render(request, "writer_dashboard/news/news_comments.html", {
        "news": news,
        "comments": comments
    })


@login_required
def writer_reply_to_comment(request, comment_id):
    """Template-based reply (POST with 'content'). Redirects back to referrer."""
    parent = get_object_or_404(Comment, id=comment_id)
    if request.method == "POST":
        content = (request.POST.get("content") or "").strip()
        if not content:
            messages.error(request, "متن پاسخ خالی است.")
        else:
            Comment.objects.create(
                user=request.user,
                content=content,
                content_type=parent.content_type,
                object_id=parent.object_id,
                parent=parent,
            )
            messages.success(request, "پاسخ ارسال شد.")
    return redirect(request.META.get("HTTP_REFERER", "/"))
