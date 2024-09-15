from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    """
    Команда создания пользователей
    """

    def handle(self, *args, **options):
        users_list = [
            {"email": "test@test.ru", "city": "Cheboksary", "groups": [1]},
            {"email": "test1@test.ru"},
        ]

        users_for_create = []

        for user in users_list:
            users_for_create.append(User(**user))
            users_for_create[-1].set_password("Qwerty")

        User.objects.bulk_create(users_for_create)
