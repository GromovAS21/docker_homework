from celery import shared_task
from django.utils import timezone

from materials.models import Course, Lesson
from materials.servises import send_mail_for_subscribers
from users.models import User


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


@shared_task
def check_last_login():
    """
    Проверка последнего входа пользователей, в случае если не заходил больше 30 дней, пользователь блокируется
    """
    today = timezone.now().date()
    last_login_users = User.objects.filter(is_active=True, is_superuser=False)
    for user in last_login_users:
        days_of_absence = today - user.last_login.date()
        if days_of_absence.days > 30:
            user.is_active = False
            user.save(update_fields=["is_active"])



