from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from materials.models import Course, Lesson


class CourseSerializer(ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"


class CourseDetailSerializer(ModelSerializer):
    number_of_lessons = SerializerMethodField()

    def get_number_of_lessons(self, course):
        return Course.objects.filter(lesson=course.title().count())

    class Meta:
        model = Course
        fields = ('title', 'description', )


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
