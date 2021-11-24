from django.core.management import BaseCommand
from give_to_good_hands.models import Institution, Category
from random import choice, randint
from faker import Faker

fake = Faker('pl_PL')


class Command(BaseCommand):
    def fake_institutions(self, how_many, it_name, it_type):
        for _ in range(how_many):
            name = f"{it_name} im. {fake.name()}"
            description = fake.sentence()
            f_type = it_type
            categories = Category.objects.all()
            count_categories = len(categories)

            new_institution = Institution.objects.create(name=name,
                                                         description=description,
                                                         type=f_type)
            for _ in range(randint(1, count_categories)):
                new_institution.categories.add(choice(categories))
            new_institution.save()

    def handle(self, *args, **options):
        # add fake foundations
        self.fake_institutions(25, "Fundacja", 0)

        # add fake organizations
        self.fake_institutions(25, "Organizacja", 1)

        # add fake local collections
        self.fake_institutions(25, "Zbiórka lokalna", 2)

