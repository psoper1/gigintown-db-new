from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):
    help = 'Create a custom superuser'

    def handle(self, *args, **options):
        email = 'psoper0604@gmail.com'  # Change this to the desired email address
        password = 'Goldpants42'  # Change this to the desired password

        User = get_user_model()

        if not User.objects.filter(email=email).exists():
            User.objects.create_superuser(email, email, password)
            self.stdout.write(self.style.SUCCESS('Custom superuser created successfully!'))
        else:
            self.stdout.write(self.style.SUCCESS('Custom superuser already exists.'))