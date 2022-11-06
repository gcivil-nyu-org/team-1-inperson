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
from .forms import InputForm


def register_page(request):
    form = CreateUserForm()
    context = {"form": form}
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data.get("email")).exists():
                messages.add_message(
                    request, messages.ERROR, "*Email taken, please choose another"
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
            return HttpResponse(
                "Please check your email address to complete registration"
            )
            # messages.success(request, "Account Succesfully Created!")
            # return redirect("/accounts/login")
    return render(request, "register.html", context)


def login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            # TODO: DELETE
            print("user is not None")
            login(request, user)
            return redirect("home")
        else:
            messages.info(request, "Incorrect username or password")

    context = {}
    # TODO: DELTE
    print("user is None")
    return render(request, "login.html", context)


def help_page(request):
    form = InputForm()
    context = {"helpform": form}
    return render(request, "help.html", context)


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
