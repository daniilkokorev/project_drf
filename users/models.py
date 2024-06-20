from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    name = None
    email = models.EmailField(verbose_name="Email", unique=True,)
    phone = models.CharField(verbose_name="Телефон", max_length=35, **NULLABLE)
    city = models.CharField(verbose_name="Город", max_length=35, **NULLABLE)
    avatar = models.ImageField(upload_to="users/media", verbose_name="Аватар", **NULLABLE,)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"
