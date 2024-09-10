from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from materials.models import Course, Lesson


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курса
    """
    count_lessons = SerializerMethodField()

    class Meta:
        model = Course
        fields = "__all__"

    def get_count_lessons(self, obj):
        """
        Возвращает количество уроков в курсе
        """
        return Lesson.objects.filter(course=obj).count()


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели урока
    """
    class Meta:
        model = Lesson
        fields = "__all__"

