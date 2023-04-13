from .models import CommentModel

from django import forms
from .models import CommentModel

# form


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ["content"]
