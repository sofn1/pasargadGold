# admin_dashboard/forms.py
from django import forms
from django.core.exceptions import ValidationError
from products.models.brand import Brand
from products.models.product import Product
from banners.models import Banner
from heros.models import Hero
from blogs.models import Blog
from news.models import News

# --- Shared Widgets ---
class RichTextarea(forms.Textarea):
    def __init__(self, attrs=None):
        default_attrs = {'class': 'rich-text'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)


# --- BLOG & NEWS ---
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = [
            'name', 'english_name', 'category_id',
            'writer', 'writer_name', 'writer_profile',
            'publish_time', 'read_time',
            'short_description', 'content',
            'view_image', 'rel_news', 'rel_blogs', 'rel_products'
        ]
        widgets = {
            'content': RichTextarea(),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'rel_news': forms.Textarea(attrs={'rows': 2}),
            'rel_blogs': forms.Textarea(attrs={'rows': 2}),
            'rel_products': forms.Textarea(attrs={'rows': 2}),
        }


class NewsForm(forms.ModelForm):
    class Meta:
        model = News
        fields = [
            'name', 'english_name', 'category_id',
            'writer', 'writer_name', 'writer_profile',
            'publish_time', 'read_time',
            'short_description', 'content',
            'view_image', 'rel_news', 'rel_blogs', 'rel_products'
        ]
        widgets = {
            'content': RichTextarea(),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'rel_news': forms.Textarea(attrs={'rows': 2}),
            'rel_blogs': forms.Textarea(attrs={'rows': 2}),
            'rel_products': forms.Textarea(attrs={'rows': 2}),
        }


# --- BANNER & HERO ---
class BannerForm(forms.ModelForm):
    class Meta:
        model = Banner
        fields = ['title', 'image', 'link', 'position', 'is_active', 'priority', 'button_text']


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['title', 'subtitle', 'background_image', 'cta_text', 'cta_link', 'overlay_color', 'is_active']


# --- BRAND & PRODUCT ---
class BrandForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ['name', 'description', 'image']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            'name', 'english_name', 'category_id',
            'price', 'featured', 'is_active',
            'owner_name', 'owner_profile',
            'short_description', 'description',
            'features', 'view_image', 'images',
            'rel_news', 'rel_blogs', 'rel_products',
            'brand'
        ]
        widgets = {
            'description': RichTextarea(),
            'short_description': forms.Textarea(attrs={'rows': 3}),
            'features': forms.Textarea(attrs={'rows': 4}),
            'images': forms.Textarea(attrs={'rows': 4}),
            'rel_news': forms.Textarea(attrs={'rows': 2}),
            'rel_blogs': forms.Textarea(attrs={'rows': 2}),
            'rel_products': forms.Textarea(attrs={'rows': 2}),
        }

    def clean_features(self):
        data = self.cleaned_data['features']
        if isinstance(data, str):
            try:
                import json
                data = json.loads(data)
            except Exception:
                raise ValidationError("Invalid JSON for features.")
        return data

    def clean_images(self):
        data = self.cleaned_data['images']
        if isinstance(data, str):
            try:
                import json
                data = json.loads(data)
            except Exception:
                raise ValidationError("Invalid JSON for images.")
            if not isinstance(data, list):
                raise ValidationError("Images must be a list.")
            if len(data) > 5:
                raise ValidationError("You can upload up to 5 images.")
        return data


class CategoryForm(forms.Form):
    name = forms.CharField(max_length=255, label="Category Name (Persian)")
    english_name = forms.CharField(max_length=255, label="Category Name (English)", required=False)
