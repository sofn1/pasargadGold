import openpyxl
from io import BytesIO
from datetime import timedelta
from news.models.news import News
from blogs.models.blog import Blog
from django.shortcuts import render
from django.utils.timezone import now
from django.db.models import Avg, Count
from django.views.generic import TemplateView
from django.http import Http404, HttpResponse
from django.db.models.functions import TruncDate
from django.contrib.auth.decorators import login_required, user_passes_test


@login_required
@user_passes_test(lambda u: getattr(u, "role", "") == "writer")
def writer_dashboard_home(request):
    return render(request, 'writer_dashboard/dashboard.html')


# -------- Summary (template page) --------
class WriterDashboardSummaryPage(TemplateView):
    template_name = "writer_dashboard/summary.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, "role", "") != "writer":
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        u = self.request.user
        ctx = super().get_context_data(**kwargs)

        blogs = Blog.objects.filter(writer=u)
        news = News.objects.filter(writer=u)

        ctx["total_blogs"] = blogs.count()
        ctx["avg_blog_read_time"] = blogs.aggregate(avg=Avg("read_time"))["avg"] or 0
        ctx["last_blog"] = blogs.order_by("-publish_time").values_list("publish_time", flat=True).first()

        ctx["total_news"] = news.count()
        ctx["avg_news_read_time"] = news.aggregate(avg=Avg("read_time"))["avg"] or 0
        ctx["last_news"] = news.order_by("-publish_time").values_list("publish_time", flat=True).first()

        return ctx


# -------- SEO Assistant (template page with POST) --------
class WriterContentSEOAssistantPage(TemplateView):
    template_name = "writer_dashboard/seo_assistant.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, "role", "") != "writer":
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        title = (request.POST.get("title") or "").strip()
        content = (request.POST.get("content") or "").strip()
        keywords_raw = (request.POST.get("keywords") or "").strip()
        keywords = [k.strip() for k in keywords_raw.split(",") if k.strip()]

        words = content.split()
        word_count = len(words)

        def density(k):
            return (content.lower().count(k.lower()) / word_count * 100) if word_count else 0.0

        keyword_density = {k: density(k) for k in keywords}
        title_len = len(title.split())

        suggestions = []
        if title_len < 5:
            suggestions.append("عنوان را طولانی‌تر و توصیفی‌تر کنید.")
        if word_count < 300:
            suggestions.append("طول محتوا را برای سئوی بهتر افزایش دهید.")
        for k, d in keyword_density.items():
            if d < 1:
                suggestions.append(f"بسامد کلیدواژه «{k}» کم است (٪{d:.2f}).")
            elif d > 3:
                suggestions.append(f"بسامد کلیدواژه «{k}» زیاد است (٪{d:.2f}) و ممکن است اسپمی تلقی شود.")

        ctx = self.get_context_data(
            title=title,
            content=content,
            keywords=" , ".join(keywords),
            word_count=word_count,
            title_length=title_len,
            keyword_density=keyword_density,
            suggestions=suggestions,
        )
        return render(request, self.template_name, ctx)


# -------- Content Trends (template page) --------
class WriterContentTrendsPage(TemplateView):
    template_name = "writer_dashboard/content_trends.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, "role", "") != "writer":
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        u = self.request.user
        ctx = super().get_context_data(**kwargs)
        start = now().date() - timedelta(days=30)

        blog_counts = (
            Blog.objects.filter(writer=u, publish_time__date__gte=start)
            .annotate(day=TruncDate("publish_time"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        # Add height on each item
        ctx["blog_time_series"] = [
            {**item, "height": (item["count"] + 1) * 10} for item in blog_counts
        ]

        news_counts = (
            News.objects.filter(writer=u, publish_time__date__gte=start)
            .annotate(day=TruncDate("publish_time"))
            .values("day")
            .annotate(count=Count("id"))
            .order_by("day")
        )

        ctx["news_time_series"] = [
            {**item, "height": (item["count"] + 1) * 10} for item in news_counts
        ]

        ctx["start_date"] = start
        ctx["end_date"] = now().date()
        return ctx


# -------- Top Performers (template page) --------
class WriterTopPerformersPage(TemplateView):
    template_name = "writer_dashboard/top_performers.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated or getattr(request.user, "role", "") != "writer":
            raise Http404
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        u = self.request.user
        ctx = super().get_context_data(**kwargs)

        # If you add a 'views' field later, change ordering to '-views'
        ctx["top_blogs"] = list(
            Blog.objects.filter(writer=u).order_by("-publish_time").values("id", "name")[:5]
        )
        ctx["top_news"] = list(
            News.objects.filter(writer=u).order_by("-publish_time").values("id", "name")[:5]
        )
        return ctx


# -------- Export (template-triggered download) --------
@login_required
def writer_export_content(request):
    if getattr(request.user, "role", "") != "writer":
        raise Http404

    wb = openpyxl.Workbook()
    ws_blog = wb.active
    ws_blog.title = 'Blogs'
    blogs = Blog.objects.filter(writer=request.user)
    ws_blog.append(['ID', 'Name', 'Publish Time', 'Read Time'])
    for b in blogs:
        ws_blog.append([b.id, b.name, b.publish_time, b.read_time])

    ws_news = wb.create_sheet(title='News')
    news_qs = News.objects.filter(writer=request.user)
    ws_news.append(['ID', 'Name', 'Publish Time', 'Read Time'])
    for n in news_qs:
        ws_news.append([n.id, n.name, n.publish_time, n.read_time])

    buffer = BytesIO()
    wb.save(buffer)
    buffer.seek(0)
    response = HttpResponse(
        buffer,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = 'attachment; filename="writer_content.xlsx"'
    return response
