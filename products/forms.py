from django import forms


class ProductCreateForm(forms.Form):
    image = forms.FileField(required=False)
    name = forms.CharField(max_length=255, min_length=6)
    price = forms.IntegerField(required=False)
    description = forms.CharField(widget=forms.Textarea())


class ReviewCreateForm(forms.Form):
    text = forms.CharField(max_length=255, min_length=3)
