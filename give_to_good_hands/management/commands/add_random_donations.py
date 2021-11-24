from django.core.management import BaseCommand
from give_to_good_hands.models import Category, Institution, Donation
from django.contrib.auth.models import User
from random import randint, choice
from faker import Faker

fake = Faker('pl_PL')


class Command(BaseCommand):
    def handle(self, *args, **options):
        for _ in range(30):
            categories = Category.objects.all()
            count_categories = len(categories)
            institutions = Institution.objects.all()
            users = User.objects.all()

            quantity = randint(1, 10)
            institution = choice(institutions)
            address = fake.street_address()
            phone_number = fake.phone_number()
            city = fake.city()
            zip_code = fake.postcode()
            pick_up_date = fake.future_date()
            pick_up_time = fake.time()
            pick_up_comment = fake.sentence()
            user = choice(users).pk

            new_donation = Donation.objects.create(quantity=quantity,
                                                   institution=institution,
                                                   address=address,
                                                   phone_number=phone_number,
                                                   city=city,
                                                   zip_code=zip_code,
                                                   pick_up_date=pick_up_date,
                                                   pick_up_time=pick_up_time,
                                                   pick_up_comment=pick_up_comment,
                                                   user_id=user)

            for _ in range(randint(1, count_categories)):
                new_donation.categories.add(choice(categories))

