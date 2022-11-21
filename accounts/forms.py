from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Contact, FNameChange, LNameChange, PassWordChange


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


class FirstNameForm(ModelForm):
    class Meta:
        model = FNameChange
        fields = "__all__"


class LastNameForm(ModelForm):
    class Meta:
        model = LNameChange
        fields = "__all__"


class PasswordForm(ModelForm):
    class Meta:
        model = PassWordChange
        fields = "__all__"
