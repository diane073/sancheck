from django.db import models
from posts.models import PostModel
from django.conf import settings

# Create your models here.


class CommentModel(models.Model):
    class Meta:
        db_table = "comment_data"

    # comment 기본 모델
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=300)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="updated_at")

    def __str__(self):
        return (
            f"user={self.author}, content={self.content}, updated_at={self.updated_at}"
        )
