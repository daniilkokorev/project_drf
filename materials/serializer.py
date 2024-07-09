from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson, Subscriptions
from materials.validators import ValidateUrlVideo


class LessonSerializer(ModelSerializer):
    """
    Сериализатор уроков.
    """
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [ValidateUrlVideo(field='url')]


class CourseSerializer(ModelSerializer):
    """
    Сериализатор курсов.
    """
    lesson_count = SerializerMethodField()
    lesson = LessonSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, object):
        """Возвращает количество уроков в курсе"""
        if object.lessons.count():
            return object.lessons.count()
        return 0

    def get_subscription(self, instance):
        request = self.context.get('request')
        user = None
        if request:
            user = request.user
        return instance.subscription_set.filter(user=user).exists()


class SubscriptionsSerializer(ModelSerializer):
    """
    Сериализатор подписок.
    """
    class Meta:
        model = Subscriptions
        fields = '__all__'
