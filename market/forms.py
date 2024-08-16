from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile


class RegistrationForm(forms.Form):
    Username = forms.CharField(max_length=20)
    Mail = forms.EmailField(max_length=15)
    Password = forms.CharField(widget=forms.PasswordInput())
    Password_confirm = forms.CharField(widget=forms.PasswordInput())


class SignInForm(forms.Form):
    Mail = forms.EmailField(max_length=15)
    Password = forms.CharField(widget=forms.PasswordInput())
