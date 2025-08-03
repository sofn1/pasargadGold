from django import forms
from blogs.models.blog import Blog
from news.models.news import News


class WriterBlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'name',
            'english_name',
            'category_id',
            'view_image',
            'publish_time',
            'read_time',
            'short_description',
            'content'
        ]
        widgets = {
            'publish_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }


class WriterNewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'name',
            'english_name',
            'category_id',
            'view_image',
            'publish_time',
            'read_time',
            'short_description',
            'content'
        ]
        widgets = {
            'publish_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
