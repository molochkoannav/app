from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):
    help = 'Создаёт суперпользователя admin@gmail.com, если его ещё нет'

    def handle(self, *args, **options):
        email = 'admin@gmail.com'

        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.WARNING(f'Пользователь {email} уже существует'))
            return

        user = User.objects.create_superuser(
            email=email,
            password='1234',
            first_name='Admin',
            last_name='Admin',
        )
        self.stdout.write(self.style.SUCCESS(f'Создан суперпользователь: {user.email}'))