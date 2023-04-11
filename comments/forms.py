from .models import CommentModel

from django import forms

# form


class ProductForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        CommentModel.objects.name("USER")
        fields = ["content", "created_at"]
