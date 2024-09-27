from celery import shared_task

from materials.models import Course, Lesson
from materials.servises import send_mail_for_subscribers


@shared_task
def send_email_about_update_course(course_id):
    """
    Отправка письма об изменении курса для подписчиков
    """
    course = Course.objects.get(id=course_id)
    message = f"Информация о курсе '{course.title}' обновлена! Посмотри."
    send_mail_for_subscribers(message, course)


@shared_task
def send_email_about_create_lesson(course_id, lesson_id):
    """
    Отправка письма о добавлении урока для подписчиков
    """
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    message = f"Курс '{course.title}' обновлен! Добавлен урок {lesson.title}."
    send_mail_for_subscribers(message, course)


@shared_task
def send_mail_about_update_lesson(course_id, lesson_id):
    """
    Отправка письма об изменении урока для подписчиков
    """
    course = Course.objects.get(id=course_id)
    lesson = Lesson.objects.get(id=lesson_id)
    message = f"Информация о уроке '{lesson.title}' обновлена! Посмотри."
    send_mail_for_subscribers(message, course)


