from django.shortcuts import render
from django.views import View
from django.db.models import Sum
from give_to_good_hands.models import Institution, Donation
from give_to_good_hands.form import ContactForm, AddDonationForm, LoginForm, RegisterForm


# Create your views here.
class LandingPageView(View):
    # landing page view
    form_class = ContactForm
    template_name = 'give_7_hands_templates/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        bags = Donation.objects.all().aggregate(Sum('quantity'))
        bags = bags.get('quantity__sum')
        institutions = Institution.objects.all().count()

        # foundations paginator
        foundations_list = Institution.objects.filter(type=0).order_by('pk')

        # organizations paginator
        organizations_list = Institution.objects.filter(type=1).order_by('pk')

        # local collections paginator
        local_collections_list = Institution.objects.filter(type=2).order_by('pk')

        context = {
            'contact_form': form,
            'copyright_year': 2019,
            'bags': bags,
            'institutions': institutions,
            'foundations': foundations_list,
            'organizations': organizations_list,
            'local_collections': local_collections_list,

        }
        return render(request, self.template_name, context)


class AddDonationView(View):
    # add donation view
    form_class = AddDonationForm
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        contact_form = self.contact_form
        context = {
            'form': form,
            'contact_form': contact_form,
            'copyright_year': 2018,

        }
        return render(request, self.template_name, context)


class LoginView(View):
    # login view
    form_class = LoginForm
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        contact_form = self.contact_form
        context = {
            'form': form,
            'contact_form': contact_form,
            'copyright_year': 2018,

        }
        return render(request, self.template_name, context)


class RegisterView(View):
    # register view
    form_class = RegisterForm
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        contact_form = self.contact_form
        context = {
            'form': form,
            'contact_form': contact_form,
            'copyright_year': 2018,

        }
        return render(request, self.template_name, context)
