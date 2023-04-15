# Create your tests here.
from django.db import models
from django.conf import settings


class PostModel(models.Model):
    CATEGORY_CHOICES = [
        ("offer", "산책해주세요!"),
        ("search", "산책해줄게요!"),
    ]

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    img_path = models.ImageField(upload_to="")
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=50)
    pets = models.CharField(max_length=50)
    time = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
