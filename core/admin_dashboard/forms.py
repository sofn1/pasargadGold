# admin_dashboard/forms.py
from django import forms
from django.core.exceptions import ValidationError
from products.models.brand import Brand
from products.models.product import Product
from banners.models import Banner
from heroes.models import Hero
from blogs.models.blog import Blog
from news.models.news import News
from categories.models import Category


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


class CategoryForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="دسته والد",
        widget=forms.Select(attrs={"class": "form-select"})
    )

    class Meta:
        model = Category
        fields = ["name", "english_name", "image", "parent", "is_active"]
        labels = {
            "name": "نام دسته",
            "english_name": "نام انگلیسی (اختیاری)",
            "image": "تصویر (اختیاری)",
            "parent": "دسته والد",
            "is_active": "فعال",
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "english_name": forms.TextInput(attrs={"class": "form-control", "dir": "ltr"}),
        }


class CategoryCreateForm(CategoryForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Default active on create
        if not self.instance or not self.instance.pk:
            self.fields["is_active"].initial = True


class BrandForm(forms.ModelForm):
    """
    Reused for both create/edit.
    - On CREATE: name, description, image are required.
    - On EDIT: name, description required; image optional.
    """
    image = forms.ImageField(required=False)

    class Meta:
        model = Brand
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        is_edit = bool(self.instance and self.instance.pk)
        # image must be required only when creating
        self.fields["image"].required = not is_edit
        # name/description should be required in both modes
        self.fields["name"].required = True
        self.fields["description"].required = True


class BrandCreateForm(forms.ModelForm):
    class Meta:
        model = Brand
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }


class BrandUpdateForm(forms.ModelForm):
    # image is optional on edit:
    image = forms.ImageField(required=False)

    class Meta:
        model = Brand
        fields = ["name", "description", "image"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 4}),
        }
