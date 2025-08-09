from django import forms


class CommentForm(forms.Form):
    content = forms.CharField(
        label="دیدگاه",
        widget=forms.Textarea(attrs={"rows": 3, "placeholder": "نظر خود را بنویسید..."})
    )
    parent_id = forms.IntegerField(required=False, widget=forms.HiddenInput())
