# core/blogs/forms.py
from django import forms
from .models import Blog
from tags.models import Tag


from products.models import Category  # <-- adjust if your name differs

class BlogCreateForm(forms.ModelForm):
    # UI field for selecting a product category (not the raw ID)
    product_category = forms.ModelChoiceField(
        queryset=Category.objects.all().order_by("name"),
        label="دسته‌بندی محصول",
        required=True,
        widget=forms.Select(attrs={"class": "form-select"})
    )

    # Let user choose tags normally (your Blog already has M2M `tags`)
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all().order_by("name"),
        required=False,
        label="برچسب‌ها",
        widget=forms.SelectMultiple(attrs={"class": "form-select", "size": 6})
    )

    class Meta:
        model = Blog
        # Exclude writer fields from the form so user can’t (and shouldn’t) set them
        exclude = ("writer", "writer_name", "writer_profile", "tags", "category_id")
        # You keep every other field as-is (publish_time, read_time, etc.)

    def save(self, commit=True):
        """
        - Store the chosen category into `category_id` under the hood (no model change needed)
        - M2M tags are set by the view after instance is saved (standard Django pattern)
        """
        instance = super().save(commit=False)
        cat = self.cleaned_data.get("product_category")
        if cat:
            instance.category_id = str(cat.pk)  # or use str(cat.slug) if you prefer storing slug
        if commit:
            instance.save()
        # M2M (tags) set in the view
        return instance

