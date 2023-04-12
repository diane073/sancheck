from django.db import models
from django.utils import timezone
from posts.models import PostModel
from django.conf import settings

# Create your models here.


class CommentModel(models.Model):
    class Meta:
        db_table = "comment_data"

    # comment 기본 모델
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    posts = models.ForeignKey(PostModel, on_delete=models.CASCADE)
    content = models.CharField(max_length=500, help_text="500자를 넘었습니다.")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created at")
    updated_at = models.DateTimeField(default=timezone.now, verbose_name="updated at")

    def __str__(self):
        return f"user={self.name}, content={self.content}, updated_at={self.updated_at}"
