from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model


User = get_user_model()


class Command(BaseCommand):
    help = "Превращает существующего пользователя в суперпользователя"

    def handle(self, *args, **options):
        user = User.objects.get(email=options["user_email"])
        user.is_staff = True
        user.is_superuser = True
        user.save()
        print(f"Пользователь {options['user_email']} теперь суперпользователь")

    def add_arguments(self, parser):
        parser.add_argument(
            'user_email',
            nargs='?',
            type=str
        )
