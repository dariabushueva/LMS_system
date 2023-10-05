from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        user = User.objects.create(
            email='admin@admin.ru',
            first_name='Admin',
            is_superuser=True,
            is_staff=True,
            is_active=True,
        )

        user.set_password('123qwerty456')
        user.save()