from django.conf import settings
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CreateUserForm
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User
from .forms import (
    InputForm,
    EditFirstnameForm,
    EditLastnameForm,
    EditPasswordForm,
    DeleteAccountForm,
)
from django.contrib.auth.hashers import check_password
from django.contrib.auth import logout


def register_page(request):
    form = CreateUserForm()
    context = {"form": form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data.get("email")).exists():
                messages.add_message(
                    request, messages.ERROR, "Email taken, please choose another"
                )
                return render(request, "register.html", context)
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = "Activate your NYCAccess account!"
            mail_message = render_to_string(
                "acc_active_email.html",
                {
                    "user": user,
                    "domain": current_site.domain,
                    "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                    "token": account_activation_token.make_token(user),
                },
            )
            to_email = form.cleaned_data.get("email")
            send_mail(
                subject=mail_subject,
                message=mail_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[to_email],
            )
            # return HttpResponse(
            #     "Please check your email address to complete registration"
            # )
            return render(request, "checkEmail.html", context)
            # messages.success(request, "Account Succesfully Created!")
            # return redirect("/accounts/login")
        else:
            messages.error(request, form.errors)

    return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("/")
        else:
            messages.info(request, "Incorrect username or password")

    context = {}
    return render(request, "login.html", context)


def help_page(request):
    form = InputForm()
    context = {"helpform": form}
    if request.method == "POST":
        form = InputForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data.get("email")
            subject = form.cleaned_data.get("subject")
            user_message = form.cleaned_data.get("message")
            # message to our email
            contact_message = (
                user_email + " Sent the following message:\n" + user_message
            )
            send_mail(
                subject=subject,
                message=contact_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
            )
            # message to user email
            mail_message = render_to_string(
                "message_sent.html",
                {
                    "user": request.user,
                    "message": user_message,
                },
            )
            send_mail(
                subject="Thank you for contacting the team!",
                message=mail_message,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user_email],
            )
            messages.info(request, "We have recieved your message!")

    return render(request, "help.html", context)

def reactivate_account(request):
    context={}
    if request.method=="POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        try:
            user = User.objects.get(username=username)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        print("credentials: ", username, password,user)
        if user is None:
            messages.info(request, "User does not exist")
        elif check_password(password,user.password)==False:
            messages.info(request, "Incorrect password")
        elif user.is_active==True:
            messages.info(request, "User is already active")
        else:
            user.is_active=True
            user.save()
            messages.info(request, "Your account has been reactivated. Login to continue")
            return redirect("/accounts/login")
    return render(request,"reactivate.html",context)

def delete_account_page(request):
    form = DeleteAccountForm()
    context = {"daform": form}
    if request.method == "POST":
        form = DeleteAccountForm(request.POST)
        user = request.user
        if form.is_valid():
            pw = user.password
            entered = form.cleaned_data.get("password_confirmation")
            if check_password(entered, pw):
                user.is_active = False
                user.save()
                logout(request)
                messages.add_message(
                    request, messages.ERROR, "Account successfully deleted"
                )
                return redirect("deleted")
            else:
                messages.add_message(
                    request, messages.ERROR, "Password is incorrect. Try again"
                )
        else:
            messages.add_message(request, messages.ERROR, "Please enter your password")
    return render(request, "deleteacc.html", context)


def deleted_message(request):
    context = {}
    return render(request, "deleted.html", context)


def ispasswordbad(candidate, username, firstname, lastname, email):
    commonpasswords = ["password", "guest", "qwerty"]
    if (
        candidate == username
        or candidate == firstname
        or candidate == lastname
        or candidate == email
    ):
        return "Password is too similar to your account credentials. Try again"
    if candidate.isnumeric():
        return "Password can't be all numbers. Try again"
    if len(candidate) < 8:
        return "Password must be more than 8 characters. Try again"
    if candidate in commonpasswords:
        return "Password is too common. Try again"
    else:
        return False


def profile_page(request):
    form1 = EditFirstnameForm()
    form2 = EditLastnameForm()
    form3 = EditPasswordForm()
    context = {"fnform": form1, "lnform": form2, "pwform": form3}
    if request.method == "POST":
        form1 = EditFirstnameForm(request.POST)
        form2 = EditLastnameForm(request.POST)
        form3 = EditPasswordForm(request.POST)
        user = request.user
        if form1.is_valid():
            user.first_name = form1.cleaned_data.get("new_first_name")
            user.save()
        if form2.is_valid():
            user.last_name = form2.cleaned_data.get("new_last_name")
            user.save()
        if form3.is_valid():
            p1 = form3.cleaned_data.get("new_password")
            p2 = form3.cleaned_data.get("confirm_password")
            if p1 == p2:
                result = ispasswordbad(
                    p1, user.username, user.first_name, user.last_name, user.email
                )
                if result:
                    messages.add_message(request, messages.ERROR, result)
                else:
                    user.set_password(p1)
                    user.save()
                    messages.add_message(
                        request,
                        messages.ERROR,
                        "Password changed successfully, please log back using your new password",
                    )
            else:
                messages.add_message(
                    request, messages.ERROR, "Passwords do not match. Try again"
                )
    return render(request, "profile.html", context)


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        messages.info(request, "Account activated! You can now login")
        return redirect("login")
    else:
        return HttpResponse("Activation link is invalid!")
