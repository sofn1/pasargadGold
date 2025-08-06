from django.urls import path
from .views.blog_views import (
    BlogListView, BlogCreateView, BlogUpdateView, BlogDeleteView)
from .views.news_views import (
    NewsListView, NewsCreateView, NewsUpdateView, NewsDeleteView)
from .views.comment_views import blog_comments_view, news_comments_view
from .views.views import (
    WriterDashboardSummaryView,
    WriterContentSEOAssistant,
    WriterContentTrendsView,
    WriterTopPerformersView,
    WriterExportContentView,

    WriterBlogListCreateView,
    WriterBlogDetailView,
    WriterNewsListCreateView,
    WriterNewsDetailView,

    WriterBlogCommentsView,
    WriterNewsCommentsView,
    writer_reply_to_comment,

    writer_blog_create,
    writer_news_create, writer_dashboard_home
)


urlpatterns = [
    path('summary/', WriterDashboardSummaryView.as_view(), name='writer_summary'),
    path('seo-assistant/', WriterContentSEOAssistant.as_view(), name='writer_seo'),
    path('content-trends/', WriterContentTrendsView.as_view(), name='writer_trends'),
    path('top-performers/', WriterTopPerformersView.as_view(), name='writer_top_performers'),
    path('export/', WriterExportContentView.as_view(), name='writer_export'),
    path('blogs/', WriterBlogListCreateView.as_view(), name='writer_blog_list_create'),
    path('blogs/<int:pk>/', WriterBlogDetailView.as_view(), name='writer_blog_detail'),
    path('news/', WriterNewsListCreateView.as_view(), name='writer_news_list_create'),
    path('news/<int:pk>/', WriterNewsDetailView.as_view(), name='writer_news_detail'),
    path('blogs/<int:blog_id>/comments/', WriterBlogCommentsView.as_view(), name='writer_blog_comments'),
    path('news/<int:news_id>/comments/', WriterNewsCommentsView.as_view(), name='writer_news_comments'),
    path('comments/<int:comment_id>/reply/', writer_reply_to_comment, name='writer_comment_reply'),
    path('blogs/create/', writer_blog_create, name='writer_blog_create'),
    path('news/create/', writer_news_create, name='writer_news_create'),
    path('blogs/<int:blog_id>/comments/', blog_comments_view, name='blog_comments_html'),   # last night
    path('news/<int:news_id>/comments/', news_comments_view, name='news_comments_html'),    # last night

    path("frontend/blogs/", BlogListView.as_view(), name="blog_list"),
    path("frontend/blogs/create/", BlogCreateView.as_view(), name="blog_create"),
    path("frontend/blogs/<int:pk>/edit/", BlogUpdateView.as_view(), name="blog_edit"),
    path("frontend/blogs/<int:pk>/delete/", BlogDeleteView.as_view(), name="blog_delete"),
    path("frontend/news/", NewsListView.as_view(), name="news_list"),
    path("frontend/news/create/", NewsCreateView.as_view(), name="news_create"),
    path("frontend/news/<int:pk>/edit/", NewsUpdateView.as_view(), name="news_edit"),
    path("frontend/news/<int:pk>/delete/", NewsDeleteView.as_view(), name="news_delete"),
    path("dashboard/", writer_dashboard_home, name="dashboard"),

]
