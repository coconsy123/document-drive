from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError

from frontend.models import Account


class RegistrationForm(UserCreationForm):

    email = forms.EmailField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter email...'}))
    password1 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password...'}))
    password2 = forms.CharField(max_length=255, widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password...'}))
    firstname = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter first name...'}))
    middlename = forms.CharField(max_length=255, required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'required': False, 'placeholder': 'Enter middle name...'}))
    lastname = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter last name...'}))
  

    class Meta:
        model = Account
        fields = ('email', 'password1', 'password2', 'firstname', 'middlename', 'lastname')

    def clean_password(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password1 != password2:
            raise ValidationError("Password does not match!")
        else:
            return password1
