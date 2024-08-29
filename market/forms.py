from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm

from .models import Profile, Category, Characteristic, ProductCharacteristicValue, Comment, Question


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


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['content']


class UpdateForm(forms.ModelForm):
    city_choice = [
        ("Dnipro", "Dnipro"),
        ("Kyiv", "Kyiv"),
        ("Kharkiv", "Kharkiv"),
        ("Odesa", "Odesa"),
        ("Lviv", "Lviv"),
        ("Zaporizhzhia", "Zaporizhzhia"),
        ("Kryvyi Rih", "Kryvyi Rih"),
        ("Mykolaiv", "Mykolaiv"),
        ("Mariupol", "Mariupol"),
        ("Luhansk", "Luhansk"),
        ("Vinnytsia", "Vinnytsia"),
        ("Kherson", "Kherson"),
        ("Poltava", "Poltava"),
        ("Chernihiv", "Chernihiv"),
        ("Cherkasy", "Cherkasy"),
        ("Sumy", "Sumy"),
        ("Zhytomyr", "Zhytomyr"),
        ("Ivano-Frankivsk", "Ivano-Frankivsk"),
        ("Ternopil", "Ternopil"),
        ("Chernivtsi", "Chernivtsi"),
        ("Rivne", "Rivne"),
        ("Kropyvnytskyi", "Kropyvnytskyi"),
        ("Khmelnytskyi", "Khmelnytskyi"),
        ("Uzhhorod", "Uzhhorod")
    ]
    gender_choice = [('M', 'Male'), ('F', 'Female'),]

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }

    Gender = forms.ChoiceField(choices=gender_choice, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    Phone = forms.CharField(max_length=15, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    Country = forms.CharField(max_length=50, widget=forms.TextInput(attrs={'class': 'form-control'}), required=False)
    City = forms.ChoiceField(choices=city_choice, widget=forms.Select(attrs={'class': 'form-control'}), required=False)
    Password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    Avatar = forms.ImageField(
        required=False,
        label='Profile Picture',
        help_text='Upload a profile picture.',
        widget=forms.ClearableFileInput(attrs={'class': 'form-control-file'})
    )


