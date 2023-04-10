
# Create your tests here.
from django.db import models


class PostModel(models.Model):

    author = models.ForeignKey("USER", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=256)
    img_path = models.ImageField(upload_to='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):

        return self.name