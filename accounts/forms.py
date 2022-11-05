from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Contact


class CreateUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=25)
    last_name = forms.CharField(max_length=25)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
        ]


class InputForm(ModelForm):
    class Meta:
        model = Contact
        fields = "__all__"
