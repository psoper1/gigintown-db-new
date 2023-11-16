from django.core.management.base import BaseCommand
from database.models import Event, CustomUser

class Command(BaseCommand):
    help = 'Fix saved_by field in Event model'

    def handle(self, *args, **options):
        # Identify rows where saved_by is 0
        invalid_events = Event.objects.filter(saved_by_id=0)

        # Update or delete the rows
        valid_user = CustomUser.objects.first()  # Replace with a valid user
        invalid_events.update(saved_by=valid_user)
        # OR
        # invalid_events.delete()

        self.stdout.write(self.style.SUCCESS('Successfully fixed saved_by field'))