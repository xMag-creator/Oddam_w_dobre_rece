from django.shortcuts import render
from django.views import View
from give_to_good_hands.form import ContactForm, AddDonationForm, LoginForm, RegisterForm


# Create your views here.
class LandingPageView(View):
    form_class = ContactForm
    template_name = 'give_7_hands_templates/index.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class AddDonationView(View):
    form_class = AddDonationForm
    template_name = 'give_7_hands_templates/form.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class LoginView(View):
    form_class = LoginForm
    template_name = 'give_7_hands_templates/login.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'give_7_hands_templates/register.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)
