from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from django.contrib.auth.models import User
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

        user = request.user
        logged = False
        if user.is_authenticated:
            logged = True

        context = {
            'contact_form': form,
            'copyright_year': 2019,
            'bags': bags,
            'institutions': institutions,
            'foundations': foundations_list,
            'organizations': organizations_list,
            'local_collections': local_collections_list,
            'logged': logged,
            'header': 'index',
            'header_class': 'header--main-page',

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

        user = request.user
        logged = False
        if user.is_authenticated:
            logged = True

        context = {
            'form': form,
            'contact_form': contact_form,
            'copyright_year': 2018,
            'logged': logged,
            'header': 'form',
            'header_class': 'header--form-page',
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

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')

            user = authenticate(username=email, password=password)
            if user:
                login(request, user)
                return redirect('/')
            else:
                return redirect('/register/')


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

    def post(self, request, *args, **kwargs):
        form = RegisterForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            surname = form.cleaned_data.get('surname')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            repeat_password = form.cleaned_data.get('repeat_password')

            User.objects.create_user(username=email,
                                     first_name=name,
                                     last_name=surname,
                                     email=email,
                                     password=password)
            return redirect('/login/')
        else:
            context = {
                'form': form,

            }
            return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')
