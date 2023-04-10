from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    """User Model Definition"""

    def __str__(self) -> str:
        return self.nickname

    class PetKindChoices(models.TextChoices):
        DOG = ("dog", "강아지")
        CAT = ("cat", "고양이")
        RABBIT = ("rabbit", "토끼")
        HASMTER = ("hamster", "햄스터")
        ETC = ("etc", "그외")

    nickname = models.CharField(
        max_length=120,
    )
    address = models.CharField(
        max_length=240,
    )
    # ↓ default=False가 아니면 createsuperuser시에 에러가 뜹니다.
    is_pet_host = models.BooleanField(default=False)
    pet_kind = models.TextField(
        choices=PetKindChoices.choices,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )
