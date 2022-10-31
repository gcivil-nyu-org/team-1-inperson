from django.test import TestCase
from django.test import Client
from .views import populate_cards
from .models import Infra_type, Accessible_location, Favorite
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User


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

    def test_populate_cards(self):
        infra_2 = Infra_type.objects.create(typeID=102)
        Accessible_location.objects.create(
            infraID=1111,
            locationX="st_1",
            locationY="st_2",
            typeID=infra_2,
            isAccessible=True,
        )
        cards, addresses = populate_cards()
        # print(cards)
        # TODO: figure out why loaded cards dont seem to fit the location i created
        # Note: without infra_2 and accessible_location cards/addresses are empty strs
        self.assertNotEqual(cards, [])
        self.assertNotEqual(addresses, [])


class ModelsTests(TestCase):
    def test_Infra_type(self):
        infra = Infra_type.objects.create(typeID=101)
        test_type = Infra_type.objects.get(typeID=101)
        self.assertEqual(infra, test_type)

    def test_Infra_str(self):
        infra = Infra_type.objects.create(typeID=101, typeName="infrastructure_type")
        infra_str = infra.__str__()
        self.assertEqual(infra_str, "infrastructure_type")

    def test_accessible_location(self):
        infra_2 = Infra_type.objects.create(typeID=102)
        accessible_location = Accessible_location.objects.create(
            infraID=1111,
            locationX="st_1",
            locationY="st_2",
            typeID=infra_2,
            isAccessible=True,
        )
        one_entry = Accessible_location.objects.get(infraID=1111)
        self.assertEqual(one_entry, accessible_location)

    def test_Accessible_str(self):
        infra_2 = Infra_type.objects.create(typeID=102)
        accessible_location = Accessible_location.objects.create(
            infraID=1111,
            locationX="st_1",
            locationY="st_2",
            typeID=infra_2,
            isAccessible=True,
        )
        self.assertEqual(accessible_location.__str__(), "1111 st_1 st_2  True")
        # TODO: Ask Ames and Atul -- output string for typeID is empty str

    def test_Favorite(self):
        user = User.objects.create(username="Testuser")
        infra_2 = Infra_type.objects.create(typeID=102)
        favorite = Favorite.objects.create(
            userID=user, locationX="st_1", locationY="st_2", typeID=infra_2
        )
        one_entry = Favorite.objects.get(
            userID=user,
            locationX="st_1",
            locationY="st_2",
        )
        self.assertEqual(favorite, one_entry)
