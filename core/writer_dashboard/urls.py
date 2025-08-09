from django.urls import path

from .views.blog_views import (
    BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView
)
from .views.news_views import (
    NewsListView, NewsCreateView, NewsUpdateView, NewsDeleteView
)
from .views.comment_views import blog_comments_view, news_comments_view, writer_reply_to_comment
from .views.views import (
    writer_dashboard_home,
    WriterDashboardSummaryPage,
    WriterContentSEOAssistantPage,
    WriterContentTrendsPage,
    WriterTopPerformersPage,
    writer_export_content,
)

app_name = "writer"

urlpatterns = [
    # Dashboard
    path("dashboard/", writer_dashboard_home, name="dashboard"),

    # Analytics/Tools (template pages)
    path("summary/", WriterDashboardSummaryPage.as_view(), name="writer_summary"),
    path("seo-assistant/", WriterContentSEOAssistantPage.as_view(), name="writer_seo"),
    path("content-trends/", WriterContentTrendsPage.as_view(), name="writer_trends"),
    path("top-performers/", WriterTopPerformersPage.as_view(), name="writer_top_performers"),
    path("export/", writer_export_content, name="writer_export"),

    # Comment pages (HTML)
    path("blogs/<int:blog_id>/comments/", blog_comments_view, name="blog_comments_html"),
    path("news/<int:news_id>/comments/", news_comments_view, name="news_comments_html"),
    path("comments/<int:comment_id>/reply/", writer_reply_to_comment, name="writer_comment_reply"),

    # Blog CRUD (template)
    path("frontend/blogs/", BlogListView.as_view(), name="blog_list"),
    path("frontend/blogs/create/", BlogCreateView.as_view(), name="blog_create"),
    path("frontend/blogs/<int:pk>/edit/", BlogUpdateView.as_view(), name="blog_edit"),
    path("frontend/blogs/<int:pk>/delete/", BlogDeleteView.as_view(), name="blog_delete"),

    # News CRUD (template)
    path("frontend/news/", NewsListView.as_view(), name="news_list"),
    path("frontend/news/create/", NewsCreateView.as_view(), name="news_create"),
    path("frontend/news/<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("frontend/news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),
]
