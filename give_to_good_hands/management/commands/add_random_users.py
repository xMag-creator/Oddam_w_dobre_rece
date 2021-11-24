from django.core.management import BaseCommand
from django.contrib.auth.models import User
from faker import Faker

fake = Faker('pl_PL')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(5):
            name = fake.first_name()
            surname = fake.last_name()
            email = fake.safe_email()
            password = '12345'
            User.objects.create_user(username=email,
                                     first_name=name,
                                     last_name=surname,
                                     email=email,
                                     password=password)

