from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_lesson_count(self, object):
        """Возвращает количество уроков в курсе"""
        if object.lessons.count():
            return object.lessons.count()
        return 0


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
