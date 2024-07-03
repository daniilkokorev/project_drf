from django.contrib.auth.models import AbstractUser
from django.db import models

from materials.models import Course, Lesson

# Create your models here.

NULLABLE = {"blank": True, "null": True}


class User(AbstractUser):
    """Модель пользователя"""

    name = None
    email = models.EmailField(verbose_name="email", unique=True,)
    phone = models.CharField(verbose_name="phone", max_length=35, **NULLABLE)
    city = models.CharField(verbose_name="city", max_length=35, **NULLABLE)
    avatar = models.ImageField(upload_to="users/media", verbose_name="avatar", **NULLABLE,)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class Payment(models.Model):
    """Модель оплаты"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь",)
    amount = models.FloatField(verbose_name="Сумма оплаты",)
    payment_date = models.DateTimeField(auto_now_add=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, verbose_name='урок', **NULLABLE)
    payment_method = models.CharField(max_length=25, verbose_name='способ оплаты')

    def __str__(self):
        return f"{self.user} - {self.lesson if self.lesson else self.course}: {self.amount}"

    class Meta:
        verbose_name = "Оплата"
        verbose_name_plural = "Оплаты"
