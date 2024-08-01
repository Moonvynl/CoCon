from django import forms
from .models import Post


class PostCreateForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['description', 'content']
        widgets = {
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.FileInput(attrs={"class": "form-control"}),
        }