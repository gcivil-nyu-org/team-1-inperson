from django.test import TestCase

# Create your tests here.

class URLTests(TestCase):

    def  test_signup_page(self):
        response = self.client.get("signup/")
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.client.get("login/")
        self.assertEqual(response.status_code, 200)

