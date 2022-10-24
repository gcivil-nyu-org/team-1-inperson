from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User


class CreateUserForm(UserCreationForm):
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


class InputForm(forms.Form):
    name = forms.CharField(max_length=200)
    email = forms.CharField(max_length=200)
    message = forms.CharField(max_length=1000)