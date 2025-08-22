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
        fields = ["title", "image", "position", "priority", "is_active"]  # ← trimmed
        labels = {
            "title": "عنوان",
            "image": "تصویر",
            "position": "موقعیت",
            "priority": "اولویت",
            "is_active": "فعال",
        }
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "image": forms.ClearableFileInput(attrs={"class": "form-control", "accept": "image/*"}),
            "position": forms.Select(attrs={"class": "form-select"}),
            "priority": forms.NumberInput(attrs={"class": "form-control", "min": 0}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class HeroForm(forms.ModelForm):
    class Meta:
        model = Hero
        fields = ['title', 'subtitle', 'background_image', 'cta_text', 'cta_link', 'overlay_color', 'is_active']


# --- BRAND & PRODUCT ---
class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"   # or list explicit fields if you prefer

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # ---- Generic styling for all fields
        for name, field in self.fields.items():
            w = field.widget
            if isinstance(w, (forms.TextInput, forms.EmailInput, forms.URLInput, forms.NumberInput)):
                w.attrs.setdefault("class", "form-control")
            elif isinstance(w, forms.Textarea):
                w.attrs.setdefault("class", "form-control")
                w.attrs.setdefault("rows", 4)
            elif isinstance(w, forms.Select):
                w.attrs.setdefault("class", "form-select")
            elif isinstance(w, (forms.SelectMultiple,)):
                w.attrs.setdefault("class", "form-select")
                w.attrs.setdefault("size", "8")
            elif isinstance(w, (forms.FileInput, forms.ClearableFileInput)):
                w.attrs.setdefault("class", "form-control")
                w.attrs.setdefault("accept", "image/*")
            elif isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault("class", "form-check-input")

        # ---- Persian labels (applied only if the field exists)
        label_map = {
            "name": "نام",
            "english_name": "نام انگلیسی",
            "category": "دسته‌بندی",
            "category_id": "دسته‌بندی",
            "price": "قیمت",
            "featured": "ویژه",
            "owner_name": "نام مالک",
            "owner_profile": "پروفایل مالک",
            "short_description": "توضیح کوتاه",
            "description": "توضیحات",
            "features": "ویژگی‌ها (JSON)",
            "view_image": "تصویر اصلی",
            "image": "تصویر اصلی",
            "images": "تصاویر",
            "rel_news": "اخبار مرتبط",
            "rel_blogs": "بلاگ‌های مرتبط",
            "rel_products": "محصولات مرتبط",
            "brand": "برند",
            "is_active": "فعال",
            # اختیاری:
            "slug": "اسلاگ",
        }
        for key, label in label_map.items():
            if key in self.fields:
                self.fields[key].label = label

        # ---- Help texts / placeholders for special fields (if present)
        help_map = {
            "features": "JSON معتبر وارد کنید. مثال: {\"weight\": \"10g\", \"material\": \"gold\"}",
            "images": "در صورت JSON، آرایه‌ای از URLها. در صورت چندفایلی، چند تصویر بارگذاری کنید.",
            "owner_profile": "لینک پروفایل مالک (اختیاری).",
        }
        for key, help_text in help_map.items():
            if key in self.fields and not self.fields[key].help_text:
                self.fields[key].help_text = help_text

        placeholder_map = {
            "name": "نام محصول",
            "english_name": "English name",
            "price": "مثلاً 2500000",
            "owner_name": "نام شخص/برند مالک",
            "short_description": "توضیح خلاصه‌ای درباره محصول…",
        }
        for key, ph in placeholder_map.items():
            if key in self.fields and hasattr(self.fields[key].widget, "attrs"):
                self.fields[key].widget.attrs.setdefault("placeholder", ph)

        # ---- Tweak dropdown empty labels
        if "brand" in self.fields and isinstance(self.fields["brand"], forms.ModelChoiceField):
            self.fields["brand"].empty_label = "— انتخاب برند —"

        # Category could be called category OR category_id (ModelChoiceField)
        for cat_key in ("category", "category_id"):
            if cat_key in self.fields and isinstance(self.fields[cat_key], forms.ModelChoiceField):
                self.fields[cat_key].empty_label = "— انتخاب دسته —"

        # Minimum for price (if NumberInput)
        if "price" in self.fields and isinstance(self.fields["price"].widget, forms.NumberInput):
            self.fields["price"].widget.attrs.setdefault("min", "0")


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
