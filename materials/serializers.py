from rest_framework import serializers

from materials.models import Course, Lesson


class CourseSerializer(serializers.Serializer):
    """
    Сериализатор для модели Курса
    """
    class Meta:
        model = Course
        fields = "__all__"


class LessonSerializer(serializers.Serializer):
    """
    Сериализатор для модели урока
    """
    class Meta:
        model = Lesson
        fields = "__all__"

