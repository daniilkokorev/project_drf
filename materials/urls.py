from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonListApiView, LessonRetrieveApiView, LessonCreateApiView, \
    LessonUpdateApiView, LessonDestroyAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r'courses', CourseViewSet, basename='courses')

urlpatterns = [
                  path('lesson/', LessonListApiView.as_view(), name='lesson_list'),
                  path('lesson/<int:pk>/', LessonRetrieveApiView.as_view(), name='lesson_retrieve'),
                  path('lesson/create/', LessonCreateApiView.as_view(), name='lesson_create'),
                  path('lesson/update/<int:pk>/', LessonUpdateApiView.as_view(), name='lesson_update'),
                  path('lesson/delete/<int:pk>/', LessonDestroyAPIView.as_view(), name='lesson_delete'),
              ] + router.urls
