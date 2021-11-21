from django import forms
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from give_to_good_hands.models import Institution, Category, Donation
from re import compile


def the_same_passwords(password_one, password_two):
    if password_one != password_two:
        raise ValidationError(f"Hasła nie są takie same.")


def enough_length(password):
    if len(password) <= 8:
        raise ValidationError('Hasło jest za krótkie')


def big_letters(password):
    if sum(1 for char in password if char.isupper()) == 0:
        raise ValidationError('Hasło musi zawierać duże litery.')


def small_letters(password):
    if sum(1 for char in password if char.islower()) == 0:
        raise ValidationError('Hasło musi zawierać małe litery.')


def numbers(password):
    print(password)
    if sum(1 for char in password if char.isdigit()) == 0:
        raise ValidationError('Hasło musi zawierać cyfry.')


def special_signs(password):
    pattern = compile('[@_!#$%^&*()<>?/\|}{~:]')
    if pattern.search(password) is None:
        raise ValidationError('Hasło musi zawierać znaki specjalne.')


class ContactForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    # message = forms.CharField(widget=forms.Textarea)
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Wiadomość', 'rows': 1}))


class AddDonationForm(forms.Form):
    quantity = forms.IntegerField(min_value=1)
    categories = forms.ModelChoiceField(widget=forms.CheckboxSelectMultiple,
                                        queryset=Category.objects.all(),
                                        empty_label=None)
    institution = forms.IntegerField()
    address = forms.CharField(label='Ulica', max_length=256)
    phone_number = forms.CharField(label='Numer telefonu', max_length=16)
    city = forms.CharField(label='Miasto', max_length=128)
    zip_code = forms.CharField(label='Kod pocztowy', max_length=6)
    pick_up_date = forms.DateField(label='Data')
    pick_up_time = forms.TimeField(label='Godzina')
    pick_up_comment = forms.CharField(label='Uwagi dla kuriera', widget=forms.Textarea(attrs={'row': 5}))


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class RegisterForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    email = forms.CharField(widget=forms.EmailInput(attrs={'placeholder': 'Email'}),
                            validators=[EmailValidator(message='Błędny e-mail.', allowlist=['example.net'])])
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}),
                               validators=[enough_length, big_letters, small_letters, numbers, special_signs])
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        the_same_passwords(cleaned_data.get('password'), cleaned_data.get('repeat_password'))


class EditUserForm(forms.Form):
    name = forms.CharField(label='Imię', widget=forms.TextInput())
    surname = forms.CharField(label='Nazwisko', widget=forms.TextInput())
    email = forms.CharField(label='Email', widget=forms.EmailInput(),
                            validators=[EmailValidator(message='Błędny e-mail.', allowlist=['example.net'])])
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class NewPasswordForm(forms.Form):
    password = forms.CharField(label='Hasło',
                               widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    new_password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}),
                                   validators=[enough_length, big_letters, small_letters, numbers, special_signs])
    repeat_new_password = forms.CharField(label='Hasło',
                                          widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))

    def clean(self):
        cleaned_data = super(NewPasswordForm, self).clean()
        the_same_passwords(cleaned_data.get('new_password'), cleaned_data.get('repeat_new_password'))
