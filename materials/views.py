from django.utils.decorators import method_decorator
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from materials.models import Course, Lesson, Subscription
from materials.paginators import ViewPagination
from materials.serializers import CourseSerializer, LessonSerializer, SubscriptionSerializer
from materials.tasks import send_email_about_update_course, send_email_about_create_lesson, \
    send_mail_about_update_lesson
from users.permissions import IsModer, IsOwner


@method_decorator(name='list', decorator=swagger_auto_schema(
    operation_description="Контроллер для получения списка всех курсов"
))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(
    operation_description="Контроллер для получения конкретного курса"
))
@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="Контроллер для создания курса"
))
@method_decorator(name='update', decorator=swagger_auto_schema(
    operation_description="Контроллер для обновления информации о курсе"
))
@method_decorator(name='partial_update', decorator=swagger_auto_schema(
    operation_description="Контроллер для частичного изменения информации о курсе"
))
@method_decorator(name='destroy', decorator=swagger_auto_schema(
    operation_description="Контроллер для удаления курса"
))
class CourseViewSet(viewsets.ModelViewSet):
    """
    API эндпоинт для модели Course
    """

    serializer_class = CourseSerializer
    queryset = Course.objects.all()
    pagination_class = ViewPagination

    def get_permissions(self):
        if self.action == "create":
            self.permission_classes = (~IsModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner | IsAdminUser,)
        elif self.action == ["destroy"]:
            self.permission_classes = (~IsModer | IsOwner,)
        return super().get_permissions()

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def update(self, request, *args, **kwargs):
        course = self.get_object()
        serializer = self.get_serializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_email_about_update_course.delay(course.id)
            return Response(serializer.data)


class LessonCreateAPIView(generics.CreateAPIView):
    """
    Контроллер для создания нового урока
    """

    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, ~IsModer)

    def perform_create(self, serializer):
        """
        Добавление владельца к уроку при создании и отправке сообщения подписчикам об этом
        """
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()
        if lesson.course:
            send_email_about_create_lesson.delay(lesson.course.id, lesson.id)


class LessonListAPIView(generics.ListAPIView):
    """
    Контроллер для получения списка всех уроков
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    pagination_class = ViewPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    """
    Контроллер для получения конкретного урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)


class LessonUpdateAPIView(generics.UpdateAPIView):
    """
    Контроллер для изменения урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsModer | IsOwner)

    def perform_update(self, serializer):
        """
        Отправка сообщения подписчикам об изменении урока
        """
        lesson = self.get_object()
        serializer.save()
        send_mail_about_update_lesson.delay(lesson.course.id, lesson.id)






class LessonDestroyAPIView(generics.DestroyAPIView):
    """
    Контроллер для удаления урока
    """

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
    permission_classes = (IsAuthenticated, IsOwner | ~IsModer)


class SubscriptionViewSet(APIView):
    """
    API эндпоинт для создания подписки на курс
    """

    @swagger_auto_schema(request_body=SubscriptionSerializer)
    def post(self, request):
        """
        Создание или удаление подписки на курс
        """
        user_id = request.user
        course_id = request.data.get('course_id')
        course_item = get_object_or_404(Course, id=course_id)

        sub_item = Subscription.objects.filter(user=user_id, course=course_item)

        if sub_item.exists():
            sub_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user_id, course=course_item)
            message = "Подписка оформлена"
            send_email_about_update_course.delay(course_item.id)
        return Response({"message": message})
