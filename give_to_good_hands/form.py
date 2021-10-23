from django import forms
from django.core.validators import EmailValidator


class ContactForm(forms.Form):
    name = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Imię'}))
    surname = forms.CharField(max_length=128, widget=forms.TextInput(attrs={'placeholder': 'Nazwisko'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Wiadomość', 'rows': 1}))


class AddDonationForm(forms.Form):
    pass


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
