from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile, Category, Characteristic, ProductCharacteristicValue


class RegistrationForm(forms.Form):
    Username = forms.CharField(max_length=20)
    Mail = forms.EmailField(max_length=15)
    Password = forms.CharField(widget=forms.PasswordInput())
    Password_confirm = forms.CharField(widget=forms.PasswordInput())


class SignInForm(forms.Form):
    Mail = forms.EmailField(max_length=15)
    Password = forms.CharField(widget=forms.PasswordInput())


class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(queryset=Category.objects.all(), required=False)

    def __init__(self, *args, **kwargs):
        category = kwargs.pop('category', None)
        super().__init__(*args, **kwargs)

        self.fields.pop('category', None)

        if category:
            characteristics = Characteristic.objects.filter(category=category)
            for characteristic in characteristics:
                field_name = f"char_{characteristic.id}"
                # Filter ProductCharacteristicValue by both category and characteristic
                queryset = ProductCharacteristicValue.objects.filter(
                    product__category=category, characteristic=characteristic
                ).values('value').distinct()
                choices = [('', '---------')] + [(entry['value'], entry['value']) for entry in queryset]
                # Create a ModelChoiceField for each characteristic, showing the value
                self.fields[field_name] = forms.ChoiceField(
                    choices=choices,
                    label=characteristic.name,
                    required=False
                )
