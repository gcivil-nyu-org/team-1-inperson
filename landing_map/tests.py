from django.test import TestCase
from django.test import Client
from .views import populate_cards, index
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
    def test_views_index(self):
        response = client.get("/")
        self.assertEqual(response.resolver_match.func, index)

    def test_populate_cards_return_type(self):
        card_list = populate_cards([])
        self.assertEqual(type(card_list), list)

    def test_populate_cards(self):
        infra_2 = Infra_type.objects.create(typeID=102)
        Accessible_location.objects.create(
            infraID=1111,
            locationX="st_1",
            locationY="st_2",
            typeID=infra_2,
            isAccessible=True,
            street1="street_1",
            street2="street_2",
            borough="Somewhere",
        )
        filteredLocations = Accessible_location.objects.all()

        cards = populate_cards(filteredLocations)
        # print(cards)
        # TODO: figure out why loaded cards dont seem to fit the location i created
        # Note: without infra_2 and accessible_location cards/addresses are empty strs
        self.assertNotEqual(cards, [])


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
            street1="street_1",
            street2="street_2",
            borough="Somewhere",
        )
        one_entry = Accessible_location.objects.get(infraID=1111)
        self.assertEqual(one_entry, accessible_location)

    def test_Accessible_str(self):
        infra_2 = Infra_type.objects.create(typeID=102, typeName="infrastructure_type2")
        accessible_location = Accessible_location.objects.create(
            infraID=1111,
            locationX="st_1",
            locationY="st_2",
            typeID=infra_2,
            isAccessible=True,
            street1="street_1",
            street2="street_2",
            borough="Somewhere",
        )
        self.assertEqual(
            accessible_location.__str__(), "1111 st_1 st_2 infrastructure_type2 True"
        )
        # TODO: update with following assert after Atul's next merge
        # self.assertEqual(accessible_location.__str__(), "1111 st_1 st_2 infrastructure_type2 True")

    def test_Favorite(self):
        user = User.objects.create(username="Testuser")
        favorite = Favorite.objects.create(
            userID=user,
            locationX="st_1",
            locationY="st_2",
        )
        one_entry = Favorite.objects.get(
            userID=user,
            locationX="st_1",
            locationY="st_2",
        )
        self.assertEqual(favorite, one_entry)
