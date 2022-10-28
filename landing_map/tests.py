from django.test import TestCase
from django.test import Client
from .views import populate_cards
from django.http import HttpResponse, HttpRequest

client = Client()
# response = HttpResponse
request = HttpRequest
# Create your tests here.
class LandingURLsTests(TestCase):
    def test_home_page(self):
        response = client.get("")
        self.assertEqual(response.status_code, 200)

    # TODO: update landing url if necessary
    # def test_landing_page(self):
    #     response = client.get("landing")
    #     self.assertEqual(response.status_code, 200)


class ViewsTests(TestCase):
    # todo: resolve attribute error (see test_pop..
    # def test_views_index(self):
    #     self.assertEqual(request.resolver_match.func, index)


    def test_populate_cards_return_type(self):
        card_list, address_list = populate_cards()
        self.assertEqual(type(card_list), list)
        self.assertEqual(type(address_list), list)

    # TODO: resolve AtributeError: type object 'HttpResponse' has no attribute 'resolver_match'
    # def test_populate_cards(self):
    #     self.assertEqual(response.resolver_match.func, populate_cards)

