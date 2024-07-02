from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscriptions
from materials.paginetions import CustomPagination
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionsSerializer
from users.permissions import Moderator, IsOwner


# Create your views here.

class CourseViewSet(ModelViewSet):
    """
    API endpoint для управления курсами.
    """
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def get_permissions(self):
        """
        Переопределение прав доступа к операциям:
            - create: Запрещено для не авторизованных пользователей
            - destroy: Запрещено для пользователей с правами модератора
            - update, retrieve: Разрешено только для пользователей с правами модератора
        """
        if self.action == 'create':
            self.permission_classes = (~Moderator,)
        elif self.action in ['update', 'retrieve']:
            self.permission_classes = (Moderator | IsOwner,)
        elif self.action == 'destroy':
            self.permission_classes = (~Moderator | IsOwner,)
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    """
    API endpoint для создания урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~Moderator, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonListApiView(ListAPIView):
    """
    API endpoint для получения списка уроков.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = CustomPagination


class LessonRetrieveApiView(RetrieveAPIView):
    """
    API endpoint для получения урока по его идентификатору.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (Moderator | IsOwner, IsAuthenticated)


class LessonUpdateApiView(UpdateAPIView):
    """
    API endpoint для изменения урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (Moderator | IsOwner, IsAuthenticated)


class LessonDestroyAPIView(DestroyAPIView):
    """
    API endpoint для удаления урока.
    """
    queryset = Lesson.objects.all()
    permission_classes = (~Moderator | IsOwner, IsAuthenticated)


class SubscriptionsViewSet(ModelViewSet):
    """
    API endpoint для управления подписками.
    """
    queryset = Subscriptions.objects.all()
    serializer_class = SubscriptionsSerializer

    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course = get_object_or_404(Course, pk=course_id)

        subscription, created = Subscriptions.objects.get_or_create(user=user, course=course)
        if not created:
            subscription.delete()
            message = "Подписка удалена"
        else:
            message = "Подписка создана"

        return Response({'message': message}, status=status.HTTP_201_CREATED)
