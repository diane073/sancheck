from django.contrib import admin
from .models import CommentModel
from .forms import CommentForm

admin.site.register(CommentModel, CommentForm)
