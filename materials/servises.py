from django.core.mail import send_mail

from config.settings import EMAIL_HOST_USER
from materials.models import Subscription


def send_mail_for_subscribers(message, course):
    """
    Отправка письма подписчикам
    """
    subscriber_list = [sub.user.email for sub in Subscription.objects.filter(course=course)]
    if subscriber_list:
        send_mail(
            "Курс обновлен!!!",
            message,
            EMAIL_HOST_USER,
            subscriber_list
        )