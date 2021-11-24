from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.views import View
from django.db.models import Sum
from django.contrib.auth.models import User
from give_to_good_hands.models import Institution, Donation, Category
from give_to_good_hands.form import ContactForm, LoginForm, RegisterForm, EditUserForm, NewPasswordForm

from re import compile, match


def contact_form_processing(contact_form):
    # Send message to all admins
    if contact_form.is_valid():
        first_name = contact_form.cleaned_data.get('name')
        last_name = contact_form.cleaned_data.get('surname')
        message = contact_form.cleaned_data.get('message')

        admins = User.objects.filter(is_staff=True)
        emails = [admin.email for admin in admins]

        email = EmailMessage(f'Wiadomość od {first_name} {last_name}.', message, to=emails)
        email.send()

    return contact_form


# Create your views here.
class LandingPageView(View):
    # landing page view
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/index.html'

    def prepare_view(self, request, contact_form):
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

        context = {
            'contact_form': contact_form,
            'bags': bags,
            'institutions': institutions,
            'foundations': foundations_list,
            'organizations': organizations_list,
            'local_collections': local_collections_list,
            'logged': user.is_authenticated,
            'staff': user.is_staff,

        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        contact_form = self.contact_form
        return self.prepare_view(request, contact_form)

    def post(self, request, *args, **kwargs):
        contact_form = self.contact_form(request.POST)
        contact_form = contact_form_processing(contact_form)
        return self.prepare_view(request, contact_form)


class AddDonationView(LoginRequiredMixin, View):
    # add donation view
    # form_class = AddDonationForm
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/form.html'

    def get(self, request, *args, **kwargs):
        # form = self.form_class
        contact_form = self.contact_form

        categories = Category.objects.all()
        institutions = Institution.objects.all().order_by('pk')

        user = request.user

        context = {
            'form': 'form',
            'contact_form': contact_form,
            'logged': user.is_authenticated,
            'staff': user.is_staff,
            'categories': categories,
            'institutions': institutions,

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'donation' in request.POST:
            contact_form = self.contact_form

            user = request.user
            quantity = request.POST.get('bags')
            categories = request.POST.getlist('categories')
            institution = request.POST.get('organization')
            address = request.POST.get('address')
            phone_number = request.POST.get('phone')
            city = request.POST.get('city')
            zip_code = request.POST.get('postcode')
            pick_up_date = request.POST.get('date')
            pick_up_time = request.POST.get('time')
            pick_up_comment = request.POST.get('more_info')

            print(phone_number)

            all_ok = True
            quantity_nok = False
            try:
                quantity_of_bags = int(quantity)
            except ValueError:
                all_ok = False
                quantity_nok = True

            all_categories = Category.objects.all()
            my_institution = Institution.objects.get(pk=institution)

            category_to_add = []
            for category_name in categories:
                for category in all_categories:
                    if category_name == category.name:
                        category_to_add.append(category)

            institution_pattern = compile(r'(\d)+')
            address_pattern = compile(r'^([AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż])+\s(\d)+')
            phone_one_pattern = compile(r"(\d){3}\s(\d){3}\s(\d){3}")
            city_pattern = compile(r'^([AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż])+')
            zip_code_pattern = compile(r'(\d){2}-(\d){3}')
            text_pattern = compile(r'^([AaĄąBbCcĆćDdEeĘęFfGgHhIiJjKkLlŁłMmNnŃńOoÓóPpRrSsŚśTtUuWwYyZzŹźŻż,.:\s-])+')

            address_nok = False
            phone_nok = False
            city_nok = False
            zip_code_nok = False
            text_nok = False

            if not institution_pattern.match(institution):
                all_ok = False

            if not address_pattern.match(address):
                all_ok = False
                address_nok = True

            if not phone_one_pattern.match(phone_number):
                all_ok = False
                phone_nok = True

            if not city_pattern.match(city):
                all_ok = False
                city_nok = True

            if not zip_code_pattern.match(zip_code):
                all_ok = False
                zip_code_nok = True

            if not text_pattern.match(pick_up_comment) and pick_up_comment != "":
                all_ok = False
                text_nok = True

            if all_ok:
                new_donation = Donation.objects.create(user_id=user.pk,
                                                       quantity=quantity_of_bags,
                                                       institution=my_institution,
                                                       address=address,
                                                       phone_number=phone_number,
                                                       city=city,
                                                       zip_code=zip_code,
                                                       pick_up_date=pick_up_date,
                                                       pick_up_time=pick_up_time,
                                                       pick_up_comment=pick_up_comment)
                for category in category_to_add:
                    new_donation.categories.add(category)
                new_donation.save()
            else:
                all_categories = Category.objects.all()
                institutions = Institution.objects.all().order_by('pk')
                context = {
                    'form': 'form',
                    'contact_form': contact_form,
                    'logged': user.is_authenticated,
                    'staff': user.is_staff,
                    'categories': all_categories,
                    'institutions': institutions,
                    'all_ok': False,
                    'quantity_nok': quantity_nok,
                    'address_nok': address_nok,
                    'phone_nok': phone_nok,
                    'city_nok': city_nok,
                    'zip_code_nok': zip_code_nok,
                    'text_nok': text_nok,
                    'set_quantity': quantity,
                    'set_categories': categories,
                    'set_institution': institution,
                    'set_address': address,
                    'set_phone_number': phone_number,
                    'set_city': city,
                    'set_zip_code': zip_code,
                    'set_pick_up_date': pick_up_date,
                    'set_pick_up_time': pick_up_time,
                    'set_pick_up_comment': pick_up_comment,

                }
                return render(request, self.template_name, context)

            return redirect('confirmation')

        elif 'email_message' in request.POST:
            contact_form = self.contact_form(request.POST)
            contact_form = contact_form_processing(contact_form)
            user = request.user
            categories = Category.objects.all()
            institutions = Institution.objects.all().order_by('pk')
            context = {
                'form': 'form',
                'contact_form': contact_form,
                'logged': user.is_authenticated,
                'staff': user.is_staff,
                'categories': categories,
                'institutions': institutions,

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

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'login' in request.POST:
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

        elif 'email_message' in request.POST:
            form = self.form_class
            contact_form = self.contact_form(request.POST)
            contact_form = contact_form_processing(contact_form)
            context = {
                'form': form,
                'contact_form': contact_form,
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

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        if 'register' in request.POST:
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
                                         password=password,
                                         is_active=False,
                                         )

                link = ''
                title = "Aktywacja konta"
                body = f"Żeby aktywować konto wejdź w link podany poniżej:\n{link}"
                email = EmailMessage(title, body, email)
                email.send()

                return redirect('/login/')
            else:
                context = {
                    'form': form,

                }
                return render(request, self.template_name, context)

        elif 'email_message' in request.POST:
            form = self.form_class
            contact_form = self.contact_form(request.POST)
            contact_form = contact_form_processing(contact_form)
            context = {
                'form': form,
                'contact_form': contact_form,
            }
            return render(request, self.template_name, context)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('/')


class ConfirmationView(View):
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/form-confirmation.html'

    def get(self, request, *args, **kwargs):
        contact_form = self.contact_form

        user = request.user

        context = {
            'contact_form': contact_form,
            'logged': user.is_authenticated,
            'superuser': user.is_staff,

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        contact_form = self.contact_form(request.POST)
        contact_form = contact_form_processing(contact_form)
        user = request.user
        context = {
            'contact_form': contact_form,
            'logged': user.is_authenticated,
            'staff': user.is_staff,
            'user': user,

        }
        return render(request, self.template_name, context)


class UserProfilView(LoginRequiredMixin, View):
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/user_profil.html'

    def prepare_view(self, request, contact_form):
        user = request.user
        active_user_donations = Donation.objects.filter(user_id=user.pk, is_taken=False)
        inactive_user_donations = Donation.objects.filter(user_id=user.pk, is_taken=True)
        context = {
            'contact_form': contact_form,
            'logged': user.is_authenticated,
            'staff': user.is_staff,
            'user': user,
            'active_user_donations': active_user_donations,
            'inactive_user_donations': inactive_user_donations,

        }
        return render(request, self.template_name, context)

    def get(self, request, *args, **kwargs):
        return self.prepare_view(request, self.contact_form)

    def post(self, request, *args, **kwargs):
        contact_form = self.contact_form(request.POST)
        contact_form = contact_form_processing(contact_form)
        return self.prepare_view(request, contact_form)


class ChangeDonationStatusView(LoginRequiredMixin, View):
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/change_donation_status.html'

    def get(self, request, *args, **kwargs):
        donation_pk = kwargs.get('pk')
        donation = Donation.objects.get(pk=donation_pk)

        if donation.is_taken:
            donation.is_taken = False
        else:
            donation.is_taken = True

        donation.save()

        return redirect('/user_profil/')


class EditUserView(LoginRequiredMixin, View):
    form = EditUserForm
    password_form = NewPasswordForm
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/edit_user.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        form = self.form(initial={'name': user.first_name,
                                  'surname': user.last_name,
                                  'email': user.email})
        contact_form = self.contact_form
        password_form = self.password_form

        context = {
            'form': form,
            'contact_form': contact_form,
            'logged': user.is_authenticated,
            'staff': user.is_staff,
            'user': user,
            'password_form': password_form,

        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.user
        contact_form = self.contact_form
        password_form = self.password_form
        form = self.form
        if 'edit_data' in request.POST:
            form = self.form(request.POST)
            if form.is_valid():
                name = form.cleaned_data.get('name')
                surname = form.cleaned_data.get('surname')
                email = form.cleaned_data.get('email')
                password = form.cleaned_data.get('password')

                if authenticate(username=email, password=password):
                    edit_user = User.objects.get(username=email)
                    edit_user.first_name = name
                    edit_user.last_name = surname
                    edit_user.email = email
                    edit_user.username = email
                    edit_user.save()

                    return redirect('/')
                else:
                    context = {
                        'form': form,
                        'contact_form': contact_form,
                        'logged': user.is_authenticated,
                        'staff': user.is_staff,
                        'user': user,
                        'message': True,
                        'password_form': password_form,

                    }
                    return render(request, self.template_name, context)
            else:
                context = {
                    'form': form,
                    'contact_form': contact_form,
                    'logged': user.is_authenticated,
                    'staff': user.is_staff,
                    'user': user,
                    'password_form': password_form,
                }
                return render(request, self.template_name, context)

        elif 'new_password_data' in request.POST:
            password_form = self.password_form(request.POST)
            if password_form.is_valid():
                password = password_form.cleaned_data.get('password')
                new_password = password_form.cleaned_data.get('new_password')
                repeat_new_password = password_form.cleaned_data.get('repeat_new_password')

                if authenticate(username=user.email, password=password):
                    edit_user = User.objects.get(username=user.email)
                    edit_user.set_password(new_password)
                    edit_user.save()

                    return redirect('/')
                else:
                    context = {
                        'form': form,
                        'contact_form': contact_form,
                        'logged': user.is_authenticated,
                        'staff': user.is_staff,
                        'user': user,
                        'message_password': True,
                        'password_form': password_form,

                    }
                    return render(request, self.template_name, context)
            else:
                context = {
                    'form': form,
                    'contact_form': contact_form,
                    'logged': user.is_authenticated,
                    'staff': user.is_staff,
                    'user': user,
                    'password_form': password_form,
                }
                return render(request, self.template_name, context)

        elif 'email_message' in request.POST:
            contact_form = self.contact_form(request.POST)
            contact_form = contact_form_processing(contact_form)
            context = {
                'form': form,
                'contact_form': contact_form,
                'logged': user.is_authenticated,
                'staff': user.is_staff,
                'user': user,
                'password_form': password_form,
            }
            return render(request, self.template_name, context)


class AccountActivationView(View):
    contact_form = ContactForm
    template_name = 'give_7_hands_templates/account_activation.html'

    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass
