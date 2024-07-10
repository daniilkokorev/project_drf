from rest_framework.filters import OrderingFilter
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from materials.models import Course, Lesson
from users.models import User, Payment
from users.serializer import UserSerializer, PaymentSerializer
from users.services import create_stripe_product, create_stripe_price, create_stripe_session


# Create your views here.

class UserViewSet(ModelViewSet):
    """
    API endpoint для управления пользователями.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """
        Создание нового пользователя.
        """
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()

    def get_permissions(self):
        """
        Переопределение прав доступа к операциям:
            - create: Разрешено для всех пользователей
        """
        if self.action == 'create':
            self.permission_classes = [AllowAny]
        return super().get_permissions()


class PaymentListAPIView(ListAPIView):
    """
    API endpoint для получения списка оплат.
    """
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ("course", "lesson", "payment_method",)
    ordering_fields = ("payment_date",)


class PaymentCreateAPIView(CreateAPIView):
    """
    API endpoint для создания оплаты.
    """
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        """
        Сохранение оплаты в базу.
        """
        instance = serializer.save()
        instance.user = self.request.user

        course_id = self.request.data.get("course")
        lesson_id = self.request.data.get("lesson")

        if course_id:
            course_product = create_stripe_product(Course.objects.get(pk=course_id).title)
            course_price = create_stripe_price(instance.course.amount, course_product)
            session_id, payment_link = create_stripe_session(course_price, instance.pk)
        else:
            lesson_product = create_stripe_product(Lesson.objects.get(pk=lesson_id).title)
            lesson_price = create_stripe_price(instance.lesson.amount, lesson_product)
            session_id, payment_link = create_stripe_session(lesson_price, instance.pk)

        instance.session_id = session_id
        instance.payment_link = payment_link
        instance.save()
