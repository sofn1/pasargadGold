import re
from django.apps import apps
from .forms import CommentForm
from django.http import Http404
from accounts.models import User
from django.contrib import messages
from .models import Comment, CommentLike
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404, redirect, render


def extract_mentions(content: str):
    return re.findall(r'@(\w+)', content or "")


def _resolve_model(model_key: str):
    """
    Map short keys to real models.
    Accepts: product/blog/news
    """
    model_map = {
        "product": "products.Product",
        "blog": "blogs.Blog",
        "news": "news.News",
    }
    dotted = model_map.get(model_key.lower())
    if not dotted:
        raise Http404("Model not supported")
    app_label, model_name = dotted.split(".")
    return apps.get_model(app_label, model_name)


@login_required
def comment_page(request, model: str, object_id: int):
    """
    GET: show comments + form
    POST: create new comment or reply (when parent_id provided)
    """
    Model = _resolve_model(model)
    target = get_object_or_404(Model, pk=object_id)
    content_type = ContentType.objects.get_for_model(Model)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            content = form.cleaned_data["content"].strip()
            parent_id = form.cleaned_data.get("parent_id")
            parent = None
            if parent_id:
                parent = get_object_or_404(Comment, pk=parent_id, content_type=content_type, object_id=object_id)

            c = Comment.objects.create(
                user=request.user,
                content=content,
                content_type=content_type,
                object_id=object_id,
                parent=parent,
            )

            # mentions by @username or @phone_number (adjust to your system)
            mentioned = extract_mentions(content)
            if mentioned:
                # Example: treat mentions as phone_number usernames, customize if needed
                users = User.objects.filter(phone_number__in=mentioned)
                # (send notifications here if you have a system)
                for u in users:
                    # Placeholder:
                    print(f"📣 Notify {u.phone_number}: You were mentioned in a comment.")

            messages.success(request, "نظر ثبت شد.")
            return redirect(request.path)
        else:
            messages.error(request, "ورودی نامعتبر است.")
    else:
        form = CommentForm()

    comments = (
        Comment.objects
        .filter(content_type=content_type, object_id=object_id, parent__isnull=True)
        .select_related("user")
        .prefetch_related("children__user", "likes")
        .order_by("-created_at")
    )

    # Simple like lookup for current user
    liked_ids = set(
        CommentLike.objects.filter(user=request.user, comment_id__in=comments.values_list("id", flat=True))
        .values_list("comment_id", flat=True)
    )

    return render(request, "comments/thread.html", {
        "target": target,
        "model_key": model.lower(),
        "object_id": object_id,
        "comments": comments,
        "form": form,
        "liked_ids": liked_ids,
    })


@login_required
def comment_edit(request, pk: int):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment.content = form.cleaned_data["content"].strip()
            comment.edited = True
            comment.save(update_fields=["content", "edited", "updated_at"])
            messages.success(request, "نظر ویرایش شد.")
            # Redirect back to its thread
            return redirect("comment_thread", model=comment.content_type.model, object_id=comment.object_id)
    else:
        form = CommentForm(initial={"content": comment.content})
    return render(request, "comments/edit.html", {"form": form, "comment": comment})


@login_required
def comment_delete(request, pk: int):
    comment = get_object_or_404(Comment, pk=pk, user=request.user)
    thread_url = None
    if request.method == "POST":
        thread_url = redirect("comment_thread", model=comment.content_type.model, object_id=comment.object_id)
        comment.delete()
        messages.info(request, "نظر حذف شد.")
        return thread_url
    return render(request, "comments/delete.html", {"comment": comment})


@login_required
def toggle_like(request, comment_id: int):
    """
    POST toggle like; redirects back to the referrer.
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    like, created = CommentLike.objects.get_or_create(user=request.user, comment=comment)
    if not created:
        like.delete()
        messages.info(request, "لایک حذف شد.")
    else:
        messages.success(request, "لایک شد.")
    return redirect(request.META.get("HTTP_REFERER", "/"))
