# orders/forms.py
from django import forms
from products.models.product import Product


class CartItemForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), label="محصول")
    quantity = forms.IntegerField(min_value=1, initial=1, label="تعداد")


class CheckoutForm(forms.Form):
    address = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), label="آدرس")
    location = forms.CharField(required=False, label="موقعیت (اختیاری)")
