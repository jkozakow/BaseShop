from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from authentication.models import CustomUser


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Email", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password'}))


class RegisterForm(UserCreationForm):
    email = forms.CharField(
        label="Email",
        max_length=30,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'email'})
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password1'}),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'name': 'password2'}),
    )
    first_name = forms.CharField(
        label="First name",
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'first_name'})
    )
    last_name = forms.CharField(
        label="Last name",
        strip=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'name': 'last_name'})
    )
    address = forms.CharField(widget=forms.Textarea(attrs={'cols': 50, 'rows': 10, 'class': 'form-control',
                                                           'name': 'address'}))

    class Meta:
        model = CustomUser
        fields = ("email", "address", "first_name", "last_name")
        field_classes = {'email': UsernameField}
