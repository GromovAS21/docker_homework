from django.urls import path
from rest_framework.routers import DefaultRouter

from materials.apps import MaterialsConfig
from materials.views import CourseViewSet, LessonCreateAPIView, LessonListAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

app_name = MaterialsConfig.name

router = DefaultRouter()
router.register(r"course", CourseViewSet, basename="materials")

urlpatterns = [
    path('lesson/create/', LessonCreateAPIView.as_view(), name="lesson_create"),
    path('lesson/', LessonListAPIView.as_view(), name="lesson_list"),
    path('lesson/<int:pk>/', LessonListAPIView.as_view(), name="lesson_view"),
    path('lesson/<int:pk>/update/', LessonUpdateAPIView.as_view(), name="lesson_update"),
    path('lesson/<int:pk>/delete/', LessonDestroyAPIView.as_view(), name="lesson_delete"),
] + router.urls