from django import forms
from .models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ["name", "slug", "color", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "placeholder": "نام برچسب"}),
            "slug": forms.TextInput(attrs={"class": "form-control", "placeholder": "اسلاگ انگلیسی"}),
            "color": forms.TextInput(attrs={"class": "form-control", "placeholder": "#1C39BB"}),
            "description": forms.TextInput(attrs={"class": "form-control", "placeholder": "توضیح کوتاه"}),
        }
