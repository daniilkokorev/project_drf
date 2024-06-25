from users.apps import UsersConfig
from rest_framework.routers import DefaultRouter
from users.views import UserViewSet, PaymentListAPIView
from django.urls import path

app_name = UsersConfig.name

router = DefaultRouter()
router.register(r'user', UserViewSet, basename='user')

urlpatterns = [
    path('payment/', PaymentListAPIView.as_view(), name='payment')
] + router.urls
