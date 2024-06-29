from django.db import models

from config.settings import AUTH_USER_MODEL

# Create your models here.

NULLABLE = {"blank": True, "null": True}


class Course(models.Model):
    """Модель курса"""

    title = models.CharField(max_length=100, verbose_name="Название курса",)
    picture = models.ImageField(upload_to="materials/course", verbose_name="Изображение", **NULLABLE,)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    """Модель урока"""

    title = models.CharField(max_length=100, verbose_name="Название урока",)
    picture = models.ImageField(upload_to="materials/lesson", verbose_name="Картинка", **NULLABLE,)
    description = models.TextField(verbose_name="Описание", **NULLABLE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons", verbose_name="Курс", **NULLABLE)
    url = models.URLField(verbose_name="Ссылка на видео", **NULLABLE)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, **NULLABLE, verbose_name='владелец')

    def __str__(self):
        return f"{self.title}, курс - {self.course}"

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
