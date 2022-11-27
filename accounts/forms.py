from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Contact, EditFName, EditLName, EditPassword,DeleteAccount


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


class EditFirstnameForm(ModelForm):
    class Meta:
        model = EditFName
        fields = "__all__"


class EditLastnameForm(ModelForm):
    class Meta:
        model = EditLName
        fields = "__all__"


class EditPasswordForm(ModelForm):
    class Meta:
        model = EditPassword
        fields = "__all__"
    new_password = forms.CharField(widget=forms.PasswordInput)
    confirm_password=forms.CharField(widget=forms.PasswordInput)

class DeleteAccountForm(ModelForm):
    class Meta:
        model=DeleteAccount
        fields="__all__"
    password_confirmation=forms.CharField(widget=forms.PasswordInput)