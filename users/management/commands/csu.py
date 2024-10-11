from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    def handle(self, *args, **options):
        profile = User.objects.create(
            email="admin@test.ru",
            is_active=True,
            is_staff=True,
            is_superuser=True

        )
        profile.set_password("Qwerty")
        profile.save()