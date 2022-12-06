from django.test import TestCase
from django.test import Client
from django.core import mail
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from .forms import CreateUserForm
from .views import activate, ispasswordbad
from .models import Contact
from django.contrib.messages import get_messages
import re


# Create your tests here.

client = Client()


class URLTests(TestCase):
    def test_signup_page(self):
        response = client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

    def test_help_page(self):
        response = client.get("/accounts/help/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset(self):
        response = client.get("/accounts/password_reset/")
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done(self):
        response = client.get("/accounts/password_reset/done/")
        self.assertEqual(response.status_code, 200)

    def test_deleted_message(self):
        response = client.get("/accounts/deleted/")
        self.assertEqual(response.status_code, 200)


class RegisterTest(TestCase):
    def test_user_added_to_database(self):
        post = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        form = CreateUserForm(post)
        form.save()

    def test_passwords_dont_match(self):
        post = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_else",
        }
        form = CreateUserForm(post)
        try:
            form.save()
        except ValueError:
            self.assertTrue(True)
            return
        raise Exception("system accepted mismatched passwords")

    def test_insecure_password_fails(self):
        post = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "password",
            "password2": "password",
        }
        form = CreateUserForm(post)
        try:
            form.save()
        except ValueError:
            self.assertTrue(True)
            return
        raise Exception("system accepted insecure password")

    # to do for Simone

    # def test_response_check_email(self):
    #     c = Client()
    #     post = {
    #         "username": "realuser",
    #         "email": "snb331@nyu.edu",
    #         "first_name": "Test",
    #         "last_name": "User",
    #         "password1": "something_very_s3cur3",
    #         "password2": "something_very_s3cur3",
    #     }
    #     response = c.post("/accounts/signup/", post, follow=True)
    #     # note: form.is_valid() returns true
    #     # note: response.status_code returns 200
    #     response_text = b"Please check your email address to complete registration"
    #     self.assertEqual(response.content, response_text)

    def test_email_already_exists(self):
        c = Client()
        post1 = {
            "username": "realuser",
            "email": "snb331@nyu.edu",
            "first_name": "Test",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        response = c.post("/accounts/signup/", post1, follow=True)
        post2 = {
            "username": "anotheruser",
            "email": "snb331@nyu.edu",
            "first_name": "Test2",
            "last_name": "User2",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        response = c.post("/accounts/signup/", post1)
        response = c.post("/accounts/signup/", post2)
        messages = []
        for message in response.context["messages"]:
            check = str(message)
            messages.append(check)
        self.assertTrue("Email taken, please choose another" in messages)


class LoginTest(TestCase):
    def test_real_user_authenticates(self):
        post = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        form = CreateUserForm(post)
        form.save()
        request = client.post("/accounts/login/")
        user = authenticate(
            request, username="realuser", password="something_very_s3cur3"
        )
        self.assertNotEqual(user, None)

    def test_user_logs_in(self):
        c = Client()
        # create user
        post = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        c.post("/accounts/signup/", post, follow=True)
        # get activation email text
        email = mail.outbox[0].body
        # get confirmation link from email
        find_confirmation_link = re.findall(r"http://testserver(.+\)/)", email)
        confirmation_link = find_confirmation_link[0]
        # authenticate user
        c.get(confirmation_link, follow=True)
        # log in
        login_post = {"username": "realuser", "password": "something_very_s3cur3"}
        # TODO: not successfully logging in user, see print statement in views
        request = c.post("/accounts/login/", login_post, follow=True)
        target_redirect = [("/", 302)]
        actual_redirect = request.redirect_chain
        self.assertEqual(actual_redirect, target_redirect)

    def test_valid_username_invalid_password(self):
        post = {
            "username": "realuser2",
            "email": "someoneelse@domain.com",
            "first_name": "Test2",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        form = CreateUserForm(post)
        form.save()
        request = client.post("/accounts/login/")
        user = authenticate(request, username="realuser", password="wrong_password")
        self.assertEqual(user, None)

    def test_invalid_username_valid_password(self):
        post = {
            "username": "realuser3",
            "email": "someoneelse@domain.com",
            "first_name": "Test2",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        form = CreateUserForm(post)
        form.save()
        request = client.post("/accounts/login/")
        user = authenticate(
            request, username="realuser", password="something_very_s3cur3"
        )
        self.assertEqual(user, None)

    def test_invalid_username_invalid_password(self):
        post = {
            "username": "realuser3",
            "email": "someoneelse@domain.com",
            "first_name": "Test2",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        form = CreateUserForm(post)
        form.save()
        request = client.post("/accounts/login/")
        user = authenticate(request, username="realuser", password="wrong_password")
        self.assertEqual(user, None)


class TestActivate(TestCase):
    def test_user_not_activated(self):
        request = "something"
        uID = "123"
        token = "243"
        response = activate(request, uID, token)
        test_content = b"Activation link is invalid!"
        self.assertEqual(response.content, test_content)

    def test_user_activated(self):
        # TODO: Note to self work on authentication once activation is complete
        # create user
        c = Client()
        post = {
            "username": "realuser",
            "email": "someoneelse@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": "something_very_s3cur3",
            "password2": "something_very_s3cur3",
        }
        c.post("/accounts/signup/", post, follow=True)
        # get activation email text
        email = mail.outbox[0].body
        # get confirmation link from email
        find_confirmation_link = re.findall(r"http://testserver(.+\)/)", email)
        confirmation_link = find_confirmation_link[0]
        response_2 = c.get(confirmation_link, follow=True)
        target_redirect = [("/accounts/login/", 302)]
        actual_redirect = response_2.redirect_chain
        self.assertEqual(actual_redirect, target_redirect)


class Models_Tests(TestCase):
    def test_model_string(self):
        target_email = "someoneelse@domain.com"
        contact = Contact.objects.create(
            email=target_email, subject="the subject", message="the message"
        )
        actual_email = contact.__str__()
        self.assertEqual(actual_email, target_email)


class Testispasswordbad(TestCase):
    def test_first_same_as_password(self):
        password = "firstname"
        is_bad = ispasswordbad(password, "username", "firstname", "lastname", "email")
        self.assertTrue(str == type(is_bad))

    def test_last_same_as_password(self):
        password = "lastname"
        is_bad = ispasswordbad(password, "username", "firstname", "lastname", "email")
        self.assertTrue(str == type(is_bad))

    def test_email_same_as_password(self):
        password = "email"
        is_bad = ispasswordbad(password, "username", "firstname", "lastname", "email")
        self.assertTrue(str == type(is_bad))

    def test_password_all_numbers(self):
        password = "11111111"
        is_bad = ispasswordbad(password, "username", "firstname", "lastname", "email")
        self.assertTrue(str == type(is_bad))

    def test_password_too_short(self):
        password = "pass"
        is_bad = ispasswordbad(password, "username", "firstname", "lastname", "email")
        self.assertTrue(str == type(is_bad))

    def test_password_common(self):
        passwords = ["password", "guest", "qwerty"]
        for p in passwords:
            is_bad = ispasswordbad(p, "username", "firstname", "lastname", "email")
            self.assertTrue(str == type(is_bad))

    def test_password_accepted(self):
        password = "9asdfo8012hf"
        is_bad = ispasswordbad(password, "username", "firstname", "lastname", "email")
        self.assertFalse(is_bad)


class HelpPageTests(TestCase):
    def test_message_sent(self):
        post = {
            "email": "email@mail.domain",
            "subject": "the subject",
            "message": "the message",
        }
        c = Client()
        c.post(
            "/accounts/help/?email=email@mail.domain&subject=the subject"
            "&message=the_message",
            post,
        )
        email = mail.outbox[0].body
        target = "email@mail.domain Sent the following message:\nthe message"
        self.assertEquals(email, target)


class DeleteAccountTests(TestCase):
    def test_password_not_entered(self):
        c = Client()
        post = {"password_confirmation": ""}
        response = c.post("/accounts/deleteacc/?", post)
        message = [str(m) for m in response.context["messages"]]
        target = "Please enter your password"
        self.assertEqual(message[0], target)

    def test_account_deleted(self):
        c = Client()
        password = "something_very_s3cur3"
        user_details = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": password,
            "password2": password,
        }
        form = CreateUserForm(user_details)
        form.save()
        request = c.post("/accounts/login/")
        user = authenticate(request, username="realuser", password=password)
        c.force_login(user)
        post = {"password_confirmation": password}
        response = c.post("/accounts/deleteacc/?", post, follow=True)
        actual = response.redirect_chain
        target = [("/accounts/deleted/", 302)]
        self.assertEqual(target, actual)

    def test_password_incorrect(self):
        c = Client()
        password = "something_very_s3cur3"
        wrong_password = "something_else"
        user_details = {
            "username": "realuser",
            "email": "someone@domain.com",
            "first_name": "Test",
            "last_name": "User",
            "password1": password,
            "password2": password,
        }
        form = CreateUserForm(user_details)
        form.save()
        request = c.post("/accounts/login/")
        user = authenticate(request, username="realuser", password=password)
        c.force_login(user)
        post = {"password_confirmation": wrong_password}
        response = c.post(f"/accounts/deleteacc/?{wrong_password}", post, follow=True)
        message = [str(m) for m in response.context["messages"]]
        target = "Password is incorrect. Try again"
        self.assertEqual(message[0], target)


# class ProfilePageTests(TestCase):
#     def test_change_first(self):
#         c = Client()
#         password = "something_very_s3cur3"
#         user_details = {
#             "username": "realuser",
#             "email": "someone@domain.com",
#             "first_name": "Test",
#             "last_name": "User",
#             "password1": password,
#             "password2": password,
#         }
#         form = CreateUserForm(user_details)
#         form.save()
#         request = c.post("/accounts/login/")
#         user = authenticate(request, username="realuser", password=password)
#         c.force_login(user)
#
#         post = {'fnform':'new_first',
#                 'lnform':'User',
#                 'pwform':password}
#         request = c.post(f"/accounts/profile?fnform=new_first&lnform=User&pwform={password}", post, follow=True)
#         print(user.first_name)
# self.assertEqual()

# def test_change_last(self):
#     pass
# def test_repeat_password(self):
#     pass
# def change_password(self):
#     pass
