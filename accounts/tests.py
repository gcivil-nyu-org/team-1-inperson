from django.test import TestCase
from django.test import Client
from django.contrib.auth import login, authenticate
from .forms import CreateUserForm


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
