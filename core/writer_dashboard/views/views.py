from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from django.db.models import Count, Avg, Q
from django.utils.timezone import now
from django.http import HttpResponse
from django.contrib.contenttypes.models import ContentType
from datetime import timedelta
import openpyxl
from io import BytesIO
import textstat

from blogs.models.blog import Blog
from news.models.news import News
from comments.models import Comment
from blogs.serializers import BlogSerializer
from news.serializers import NewsSerializer
from comments.serializers import CommentSerializer
from rest_framework.decorators import api_view, permission_classes
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from writer_dashboard.forms import WriterBlogForm, WriterNewsForm


@login_required
def writer_blog_create(request):
    if request.method == 'POST':
        form = WriterBlogForm(request.POST, request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.writer_name = request.user.get_full_name()
            blog.writer_profile = ''  # optional: set profile image URL
            blog.writer = request.user
            blog.save()
            return redirect('writer_blog_list')
    else:
        form = WriterBlogForm()
    return render(request, 'writer_dashboard/blog_form.html', {'form': form})


@login_required
def writer_news_create(request):
    if request.method == 'POST':
        form = WriterNewsForm(request.POST, request.FILES)
        if form.is_valid():
            news = form.save(commit=False)
            news.writer_name = request.user.get_full_name()
            news.writer_profile = ''  # optional: set profile image URL
            news.writer = request.user
            news.save()
            return redirect('writer_news_list')
    else:
        form = WriterNewsForm()
    return render(request, 'writer_dashboard/news_form.html', {'form': form})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def writer_reply_to_comment(request, comment_id):
    try:
        parent_comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response({"error": "Parent comment not found."}, status=404)

    content = request.data.get("content")
    if not content:
        return Response({"error": "Content is required."}, status=400)

    reply = Comment.objects.create(
        user=request.user,
        content=content,
        content_type=parent_comment.content_type,
        object_id=parent_comment.object_id,
        parent=parent_comment
    )

    return Response(CommentSerializer(reply).data, status=201)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def writer_reply_to_comment(request, comment_id):
    parent_comment = Comment.objects.filter(id=comment_id).first()
    if not parent_comment:
        return Response({'error': 'Comment not found'}, status=404)

    reply_content = request.data.get('content')
    if not reply_content:
        return Response({'error': 'Reply content is required'}, status=400)

    reply = Comment.objects.create(
        user=request.user,
        content_object=parent_comment.content_object,
        content=reply_content,
        parent=parent_comment
    )

    serializer = CommentSerializer(reply)
    return Response(serializer.data, status=201)


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class WriterDashboardSummaryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'writer_permission'):
            return Response({"error": "No writing permissions assigned."}, status=403)

        summary = {}
        perm = user.writer_permission

        if perm.can_write_blogs:
            blogs = Blog.objects.filter(writer=user)
            summary['total_blogs'] = blogs.count()
            summary['blog_views'] = blogs.aggregate(total=Count('views'))['total'] or 0
            summary['avg_blog_read_time'] = blogs.aggregate(avg=Avg('readTime'))['avg'] or 0
            summary['last_blog'] = blogs.order_by('-publishTime').first().publishTime if blogs.exists() else None

        if perm.can_write_news:
            news = News.objects.filter(writer=user)
            summary['total_news'] = news.count()
            summary['news_views'] = news.aggregate(total=Count('views'))['total'] or 0
            summary['avg_news_read_time'] = news.aggregate(avg=Avg('readTime'))['avg'] or 0
            summary['last_news'] = news.order_by('-publishTime').first().publishTime if news.exists() else None

        return Response(summary)


class WriterContentSEOAssistant(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        content = request.data.get("content", "")
        title = request.data.get("title", "")
        keywords = request.data.get("keywords", [])

        word_count = len(content.split())
        keyword_density = {k: content.lower().count(k.lower()) / word_count * 100 if word_count else 0 for k in
                           keywords}
        title_length = len(title.split())

        suggestions = []
        if title_length < 5:
            suggestions.append("Consider making your title longer and more descriptive.")
        if word_count < 300:
            suggestions.append("Consider increasing the post length for better SEO.")
        for k, density in keyword_density.items():
            if density < 1:
                suggestions.append(f"Increase usage of keyword '{k}' (currently {density:.2f}%).")
            elif density > 3:
                suggestions.append(
                    f"Reduce keyword '{k}' (currently {density:.2f}%), may be flagged as keyword stuffing.")

        readability = textstat.flesch_reading_ease(content)
        reading_level = textstat.text_standard(content, float_output=False)
        sentence_count = textstat.sentence_count(content)
        syllable_count = textstat.syllable_count(content)

        tone = "informal"
        if readability < 50:
            tone = "formal"
        elif 50 <= readability <= 70:
            tone = "neutral"

        return Response({
            "word_count": word_count,
            "title_length": title_length,
            "keyword_density": keyword_density,
            "suggestions": suggestions,
            "ai_analysis": {
                "readability_score": readability,
                "estimated_reading_level": reading_level,
                "sentence_count": sentence_count,
                "syllable_count": syllable_count,
                "estimated_tone": tone
            }
        })


class WriterContentTrendsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'writer_permission'):
            return Response({"error": "No writing permissions assigned."}, status=403)

        perm = user.writer_permission
        result = {}

        days_ago = now().date() - timedelta(days=30)

        if perm.can_write_blogs:
            blog_counts = Blog.objects.filter(writer=user, publishTime__date__gte=days_ago) \
                .extra({'day': "date(publishTime)"}).values('day').annotate(count=Count('id'))
            result['blog_time_series'] = list(blog_counts)

        if perm.can_write_news:
            news_counts = News.objects.filter(writer=user, publishTime__date__gte=days_ago) \
                .extra({'day': "date(publishTime)"}).values('day').annotate(count=Count('id'))
            result['news_time_series'] = list(news_counts)

        return Response(result)


class WriterTopPerformersView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'writer_permission'):
            return Response({"error": "No writing permissions assigned."}, status=403)

        perm = user.writer_permission
        result = {}

        if perm.can_write_blogs:
            top_blogs = Blog.objects.filter(writer=user).order_by('-views')[:5].values('id', 'name', 'views')
            result['top_blogs'] = list(top_blogs)

        if perm.can_write_news:
            top_news = News.objects.filter(writer=user).order_by('-views')[:5].values('id', 'name', 'views')
            result['top_news'] = list(top_news)

        return Response(result)


class WriterExportContentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if not hasattr(user, 'writer_permission'):
            return Response({"error": "No writing permissions assigned."}, status=403)

        perm = user.writer_permission
        wb = openpyxl.Workbook()
        if perm.can_write_blogs:
            ws_blog = wb.active
            ws_blog.title = 'Blogs'
            blogs = Blog.objects.filter(writer=user)
            ws_blog.append(['ID', 'Name', 'Views', 'ReadTime'])
            for b in blogs:
                ws_blog.append([b.id, b.name, b.views, b.readTime])
        if perm.can_write_news:
            ws_news = wb.create_sheet(title='News')
            news = News.objects.filter(writer=user)
            ws_news.append(['ID', 'Name', 'Views', 'ReadTime'])
            for n in news:
                ws_news.append([n.id, n.name, n.views, n.readTime])

        buffer = BytesIO()
        wb.save(buffer)
        buffer.seek(0)
        response = HttpResponse(buffer,
                                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = 'attachment; filename="writer_content.xlsx"'
        return response


class WriterBlogListCreateView(generics.ListCreateAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class WriterBlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BlogSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return Blog.objects.filter(writer=self.request.user)


class WriterNewsListCreateView(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)

    def perform_create(self, serializer):
        serializer.save(writer=self.request.user)


class WriterNewsDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return News.objects.filter(writer=self.request.user)


class WriterBlogCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, blog_id):
        keyword = request.query_params.get("search")
        try:
            blog = Blog.objects.get(id=blog_id, writer=request.user)
        except Blog.DoesNotExist:
            return Response({"error": "Blog not found or access denied."}, status=404)

        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(Blog), object_id=blog.id)
        if keyword:
            comments = comments.filter(Q(content__icontains=keyword) | Q(user__username__icontains=keyword))

        comments = comments.order_by('-created_at')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)


class WriterNewsCommentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, news_id):
        keyword = request.query_params.get("search")
        try:
            news = News.objects.get(id=news_id, writer=request.user)
        except News.DoesNotExist:
            return Response({"error": "News not found or access denied."}, status=404)

        comments = Comment.objects.filter(content_type=ContentType.objects.get_for_model(News), object_id=news.id)
        if keyword:
            comments = comments.filter(Q(content__icontains=keyword) | Q(user__username__icontains=keyword))

        comments = comments.order_by('-created_at')
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(comments, request)
        serializer = CommentSerializer(page, many=True)
        return paginator.get_paginated_response(serializer.data)
