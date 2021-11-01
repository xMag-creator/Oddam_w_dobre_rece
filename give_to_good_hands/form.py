from django import forms
from django.core.validators import EmailValidator
from give_to_good_hands.models import Institution, Category, Donation


class ContactForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
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
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    repeat_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz hasło'}))


class EditUserForm(forms.Form):
    name = forms.CharField(label='Imię', widget=forms.TextInput())
    surname = forms.CharField(label='Nazwisko', widget=forms.TextInput())
    email = forms.CharField(label='Email', widget=forms.EmailInput(),
                            validators=[EmailValidator(message='Błędny e-mail.', allowlist=['example.net'])])
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))


class NewPasswordForm(forms.Form):
    password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Hasło'}))
    new_password = forms.CharField(label='Hasło', widget=forms.PasswordInput(attrs={'placeholder': 'Nowe hasło'}))
    repeat_new_password = forms.CharField(label='Hasło',
                                          widget=forms.PasswordInput(attrs={'placeholder': 'Powtórz nowe hasło'}))
