from .models import CommentModel

from django import forms

# form


class CommentForm(forms.ModelForm):
    class Meta:
        model = CommentModel
        fields = ["content", "created_at"]

    def __str__(self):
        return self.name
