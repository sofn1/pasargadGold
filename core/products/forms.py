from django import forms
from .models.product import Product
from django.contrib.postgres.fields import JSONField


class ProductAdminForm(forms.ModelForm):
    features = forms.JSONField()

    class Meta:
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.initial['features'] = self.instance.features