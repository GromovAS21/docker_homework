from django.core.management import BaseCommand

from materials.models import Lesson, Course
from users.models import User, Payment


class Command(BaseCommand):
    """
    Команда создания платежей
    """

    def handle(self, *args, **options):
        payment_list = [
            {"user_id": 1, "paid_course_id": 1, "amount": 50000, "method": 'Наличные'},
            {"user_id": 1, "paid_lesson_id": 1, "amount": 20000},
            {"user_id": 2, "paid_course_id": 2, "amount": 400000},
            {"user_id": 2, "paid_lesson_id": 2, "amount": 10000, "method": 'Наличные'}
        ]

        payment_for_create = []
        for payment in payment_list:
            payment_for_create.append(Payment(**payment))

        Payment.objects.bulk_create(payment_for_create)
