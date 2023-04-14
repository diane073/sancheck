from django import forms
from .models import PostModel


class PostForm(forms.ModelForm):
    class Meta:
        model = PostModel
        fields = ['category', 'title', 'description', 'img_path']



