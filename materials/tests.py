from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from materials.models import Course, Lesson, Subscriptions
from users.models import User


class LessonTestCase(APITestCase):
    """
    Тесты для уроков.
    """

    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="testcourse", description="Tests Courses")
        self.lesson = self.course.lessons.create(title="TestLesson", description="Test Lesson", course=self.course,
                                                 owner=self.user,
                                                 url="https://example.com/lesson")

    def test_lesson_retrieve(self):
        url = reverse("materials:lesson_retrieve", args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), self.lesson.title)
        self.assertEqual(data.get("description"), "Test Lesson")
        self.assertEqual(data.get("course"), self.course.pk)
        self.assertEqual(data.get("owner"), self.user.pk)
        self.assertEqual(data.get("url"), self.lesson.url)

    def test_lesson_create(self):
        url = reverse("materials:lesson_create")
        data = {
            "title": "New Test Lesson",
            "description": "New Test Lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
            "url": "https://www.youtube.com/watch"
        }
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)
        self.assertEqual(data.get("title"), "New Test Lesson")
        self.assertEqual(data.get("description"), "New Test Lesson")
        self.assertEqual(data.get("course"), self.course.pk)
        self.assertEqual(data.get("owner"), self.user.pk)
        self.assertEqual(data.get("url"), "https://www.youtube.com/watch")

    def test_lesson_update(self):
        url = reverse("materials:lesson_update", args=(self.lesson.pk,))
        data = {
            "title": "Updated Test Lesson",
            "description": "Updated Test Lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
            "url": "https://www.youtube.com/watch"
        }
        response = self.client.patch(url, data)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("title"), "Updated Test Lesson")
        self.assertEqual(data.get("description"), "Updated Test Lesson")
        self.assertEqual(data.get("course"), self.course.pk)
        self.assertEqual(data.get("owner"), self.user.pk)
        self.assertEqual(data.get("url"), "https://www.youtube.com/watch")

    def test_lesson_delete(self):
        url = reverse("materials:lesson_delete", args=(self.lesson.pk,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        url = reverse("materials:lesson_list")
        data = {
            "title": "New Test Lesson",
            "description": "New Test Lesson",
            "course": self.course.pk,
            "owner": self.user.pk,
            "url": "https://www.youtube.com/watch"
        }
        response = self.client.get(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(data.get("title"), "New Test Lesson")
        self.assertEqual(data.get("description"), "New Test Lesson")
        self.assertEqual(data.get("course"), self.course.pk)
        self.assertEqual(data.get("owner"), self.user.pk)
        self.assertEqual(data.get("url"), "https://www.youtube.com/watch")


class SubscriptionsTestCase(APITestCase):
    """
    Тесты для подписок.
    """
    def setUp(self):
        self.user = User.objects.create(email="test@mail.ru")
        self.client.force_authenticate(user=self.user)
        self.course = Course.objects.create(title="test_course", description="Tests Courses")

    def test_subscription_create(self):
        """
        Проверка создания подписки.
        """
        data = {"course": self.course.pk}
        url = reverse("materials:subscription-list")
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Subscriptions.objects.all().count(), 1)
        self.assertEqual(Subscriptions.objects.filter(course=self.course).exists(), True)
