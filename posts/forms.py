from django import forms
from .models import PostModel


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['category', 'title', 'time', 'pets', 'description', 'img_path']
        widgets = {
            "category": forms.Select(
                attrs={"class": "form-control"},
            ),
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "img_path": forms.FileInput(attrs={"class": "form-control"}),
            "pets": forms.TextInput(attrs={"class": "form-control"}),
            "time": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control", "style":"height: 300px"}),
        }

