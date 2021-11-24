from django.core.management import BaseCommand
from give_to_good_hands.models import Institution


class Command(BaseCommand):
    def handle(self, *args, **options):
        Institution.objects.all().delete()
