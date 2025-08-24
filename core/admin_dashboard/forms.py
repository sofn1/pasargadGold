# admin_dashboard/forms.py
import json
from django import forms
from heroes.models import Hero
from banners.models import Banner
from news.models.news import News
from blogs.models.blog import Blog
from categories.models import Category
from products.models.brand import Brand
from products.models.product import Product
from django.core.exceptions import ValidationError
from accounts.models import User, Writer, WriterPermission, Seller


# --- sellers and writers ---
class AdminCreateUserBaseForm(forms.Form):
    phone_number = forms.CharField(label="شماره موبایل", max_length=15)
    password = forms.CharField(label="رمز عبور", widget=forms.PasswordInput)
    first_name = forms.CharField(label="نام", max_length=64)
    last_name = forms.CharField(label="نام خانوادگی", max_length=64)
    age = forms.IntegerField(label="سن", min_value=0)


def clean_phone_number(self):
    phone = self.cleaned_data["phone_number"].strip()
    if User.objects.filter(phone_number=phone).exists():
        raise ValidationError("این شماره موبایل قبلاً ثبت شده است.")
    return phone


class AdminUpdateUserBaseForm(forms.Form):
    first_name = forms.CharField(label="نام", max_length=64)
    last_name = forms.CharField(label="نام خانوادگی", max_length=64)
    age = forms.IntegerField(label="سن", min_value=0)


# ---------------------- Writer ----------------------
class AdminCreateWriterForm(AdminCreateUserBaseForm):
    email = forms.EmailField(label="ایمیل")
    about_me = forms.CharField(label="درباره من", widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(label="تصویر پروفایل", required=False)
    can_write_blogs = forms.BooleanField(label="مجوز نوشتن وبلاگ", required=False)
    can_write_news = forms.BooleanField(label="مجوز نوشتن خبر", required=False)


class AdminUpdateWriterForm(AdminUpdateUserBaseForm):
    email = forms.EmailField(label="ایمیل")
    about_me = forms.CharField(label="درباره من", widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(label="تصویر پروفایل", required=False)
    can_write_blogs = forms.BooleanField(label="مجوز نوشتن وبلاگ", required=False)
    can_write_news = forms.BooleanField(label="مجوز نوشتن خبر", required=False)


# ---------------------- Seller ----------------------
class AdminCreateSellerForm(AdminCreateUserBaseForm):
    email = forms.EmailField(label="ایمیل")
    about_us = forms.CharField(label="درباره ما", widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(label="تصویر پروفایل", required=False)
    address = forms.CharField(label="آدرس", widget=forms.Textarea)
    location = forms.CharField(label="موقعیت (اختیاری)", required=False)
    business_name = forms.CharField(label="نام کسب‌وکار", max_length=128)
    business_code = forms.CharField(label="کد کسب‌وکار", max_length=64)


class AdminUpdateSellerForm(AdminUpdateUserBaseForm):
    email = forms.EmailField(label="ایمیل")
    about_us = forms.CharField(label="درباره ما", widget=forms.Textarea, required=False)
    profile_image = forms.ImageField(label="تصویر پروفایل", required=False)
    address = forms.CharField(label="آدرس", widget=forms.Textarea)
    location = forms.CharField(label="موقعیت (اختیاری)", required=False)
    business_name = forms.CharField(label="نام کسب‌وکار", max_length=128)
    business_code = forms.CharField(label="کد کسب‌وکار", max_length=64)


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
    # Change the category_id field to handle multiple selections
    category_id = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,  # Set to True or False based on your requirements
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        label="دسته‌بندی"
    )

    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'}),
        label="دسته‌بندی"
    )

    images = forms.JSONField(required=False)

    class Meta:
        model = Product
        fields = "__all__"
        fields = ['name', 'english_name', 'categories', 'category_id', 'brand', 'price', 'featured', 'is_active',
                  'owner_name',
                  'owner_profile', 'short_description', 'description', 'features', 'view_image', 'rel_blogs',
                  'rel_news', 'rel_products']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "price" in self.fields:
            # Render as text so commas don’t break HTML5 number input
            self.fields["price"].widget = forms.TextInput(
                attrs={
                    "class": "form-control",
                    "dir": "ltr",
                    "inputmode": "numeric",  # mobile numeric keypad
                    "placeholder": "مثلاً 2,500,000",
                }
            )
            self.fields["price"].label = "قیمت (تومان)"

        # ---------- Base widget classes ----------
        for name, field in self.fields.items():
            w = field.widget
            if isinstance(w, (forms.TextInput, forms.EmailInput, forms.URLInput, forms.NumberInput)):
                w.attrs.setdefault("class", "form-control")
            elif isinstance(w, forms.Textarea):
                w.attrs.setdefault("class", "form-control")
                w.attrs.setdefault("rows", 4)
            elif isinstance(w, forms.Select):
                w.attrs.setdefault("class", "form-select")
            elif isinstance(w, forms.SelectMultiple):
                w.attrs.setdefault("class", "form-select")
                w.attrs.setdefault("size", "8")
            elif isinstance(w, (forms.FileInput, forms.ClearableFileInput)):
                w.attrs.setdefault("class", "form-control")
                w.attrs.setdefault("accept", "image/*")
            elif isinstance(w, forms.CheckboxInput):
                w.attrs.setdefault("class", "form-check-input")

        # ---------- Persian labels ----------
        label_map = {
            "name": "نام",
            "english_name": "نام انگلیسی",
            "category": "دسته‌بندی",
            "category_id": "دسته‌بندی",
            "price": "قیمت (تومان)",
            "featured": "ویژه",
            "owner_name": "نام مالک",
            "owner_profile": "پروفایل مالک",
            "short_description": "توضیح کوتاه",
            "description": "توضیحات",
            "features": "ویژگی‌ها (JSON)",
            "view_image": "تصویر اصلی",
            "images": "تصاویر",
            "rel_news": "اخبار مرتبط",
            "rel_blogs": "بلاگ‌های مرتبط",
            "rel_products": "محصولات مرتبط",
            "brand": "برند",
            "is_active": "فعال",
            "slug": "اسلاگ",
        }
        for key, label in label_map.items():
            if key in self.fields:
                self.fields[key].label = label

        # ---------- Help / placeholders ----------
        help_map = {
            "owner_profile": "لینک پروفایل مالک (اختیاری).",
        }
        for key, txt in help_map.items():
            if key in self.fields and not self.fields[key].help_text:
                self.fields[key].help_text = txt

        placeholder_map = {
            "name": "نام محصول",
            "english_name": "English name",
            "price": "مثلاً 2,500,000",
            "owner_name": "نام شخص/برند مالک",
            "short_description": "توضیح خلاصه‌ای درباره محصول…",
        }
        for key, ph in placeholder_map.items():
            if key in self.fields and hasattr(self.fields[key].widget, "attrs"):
                self.fields[key].widget.attrs.setdefault("placeholder", ph)

        # ---------- Empty labels for dropdowns ----------
        if "brand" in self.fields and isinstance(self.fields["brand"], forms.ModelChoiceField):
            self.fields["brand"].empty_label = "— انتخاب برند —"
        for cat_key in ("category", "category_id"):
            if cat_key in self.fields and isinstance(self.fields[cat_key], forms.ModelChoiceField):
                self.fields[cat_key].empty_label = "— انتخاب دسته —"

        # ---------- Price: server-side comma formatting (no JS) ----------
        if "price" in self.fields:
            self.fields["price"].widget.attrs.setdefault("inputmode", "numeric")
            self.fields["price"].widget.attrs.setdefault("dir", "ltr")
            raw = self.initial.get("price")
            if raw is None and getattr(self.instance, "pk", None):
                raw = getattr(self.instance, "price", None)
            try:
                if raw not in (None, ""):
                    self.initial["price"] = f"{int(raw):,}"
            except Exception:
                pass
            # optional min
            if isinstance(self.fields["price"].widget, forms.NumberInput):
                self.fields["price"].widget.attrs.setdefault("min", "0")

        # ---------- Hide raw images JSON (we manage uploads via extra_images in the view/template) ----------
        if "images" in self.fields:
            self.fields["images"].widget = forms.HiddenInput()

        # ---------- features initial as JSON string (for the repeater) ----------
        if "features" in self.fields:
            # Ensure initial is a JSON string (template reads it for the repeater)
            init_val = self.initial.get("features", None)
            if init_val is None and getattr(self.instance, "pk", None):
                init_val = getattr(self.instance, "features", None)
            try:
                if isinstance(init_val, (dict, list)):
                    self.initial["features"] = json.dumps(init_val, ensure_ascii=False)
                elif isinstance(init_val, str) and init_val.strip():
                    # Keep as-is (assume valid JSON); if not, clean_features will handle.
                    self.initial["features"] = init_val
                else:
                    self.initial["features"] = "{}"
            except Exception:
                self.initial["features"] = "{}"

    # ---------- Cleaners ----------

    def clean_price(self):
        price = self.cleaned_data.get("price")
        if isinstance(price, str):
            price = price.replace(",", "").strip()
            price = int(price) if price.isdigit() else price
        return price

    def clean_features(self):
        """
        Accept either a dict (from JSONField) or a JSON string (from the repeater hidden textarea).
        """
        val = self.cleaned_data.get("features")
        if isinstance(val, dict):
            return val
        if isinstance(val, str):
            val = val.strip()
            if not val:
                return {}
            try:
                parsed = json.loads(val)
                if isinstance(parsed, dict):
                    return parsed
                # if user passed a list or other type, coerce to {}
                return {}
            except Exception:
                raise forms.ValidationError("فرمت ویژگی‌ها معتبر نیست. لطفاً به صورت JSON وارد کنید.")
        return {}


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
