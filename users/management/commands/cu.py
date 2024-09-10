from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда создания пользователей
    """
    def handle(self, *args, **options):
        users_list = [
            {"email": "test@test.ru", "password": "Qwerty", "city": "Cheboksary"},
            {"email": "test1@test.ru", "password": "Qwerty"}
        ]

        users_for_create = []

        for user in users_list:
            users_for_create.append(User(**user))

        User.objects.bulk_create(users_for_create)