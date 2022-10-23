from django.test import TestCase
from django.test import Client
from .forms import CreateUserForm

# Create your tests here.

client = Client()
class URLTests(TestCase):
    def  test_signup_page(self):
        response = client.get("/accounts/signup/")
        self.assertEqual(response.status_code, 200)


    def test_login_page(self):
        response = client.get("/accounts/login/")
        self.assertEqual(response.status_code, 200)

class RegisterTest(TestCase):
    username = 'testy'
    email = 'testy@fake.com'
    first_name = 'Test'
    last_name = 'User'
    password1 = 'password'
    bad_password2 = 'notpassword'
    def test_user_added_to_database(self):
        response = client.post("/accounts/login/")
        print(response)
        self.assertEqual(4,4)

    def test_passwords_match(self):
        # TODO
        pass

    def test_passwords_dont_match(self):
        # TODO
        pass

class LoginTest(TestCase):
    good_username = 'realuser'
    good_password = 'password'
    bad_unsername = 'baduser'
    bad_password = 'notpassword'
    # TODO: add user to database to test


    def test_real_user_authenticates(self):
        # TODO
        pass

    def test_valid_username_invalid_password(self):
        # TODO
        pass

    def test_invalid_username_valid_password(self):
        # TODO
        pass

    def test_invalid_username_invalid_password(self):
        # TODO
        pass
