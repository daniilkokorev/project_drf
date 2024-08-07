from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView, \
    get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson, Subscriptions
from materials.paginations import CustomPagination
from materials.serializer import CourseSerializer, LessonSerializer, SubscriptionsSerializer
from users.permissions import Moderator, IsOwner
from materials.tasks import course_update_message


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

    def perform_update(self, serializer):
        """
        Обновляет курс и отправляет сообщение о его изменении в очередь Celery.
        """
        serializer.save()
        course = serializer.save()
        course_id = course.id
        course_update_message.delay(course_id)


class LessonCreateApiView(CreateAPIView):
    """
    API endpoint для создания урока.
    """
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (~Moderator, IsAuthenticated)

    def perform_create(self, serializer):
        """
        Присваивает созданному уроку текущего пользователя.
        """
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
    serializer_class = SubscriptionsSerializer

    def post(self, *args, **kwargs):
        """
        Проверка наличия курса и создание или удаление подписки.
        """
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)

        subscription, created = Subscriptions.objects.get_or_create(user=user, course=course_item)
        if not created:
            subscription.delete()
            message = 'Подписка удалена'
        else:
            message = 'Подписка добавлена'
        return Response({"message": message})


