from django.test import TestCase
from django.test import Client
from decouple import config
from .views import populate_cards, index, landingpage
from .models import Infra_type, Accessible_location, Favorite
from django.http import HttpResponse, HttpRequest
from django.contrib.auth.models import User
import requests


client = Client()
# response = HttpResponse
request = HttpRequest


# Create your tests here.
class UtilsTests(TestCase):
    # def test_get_location(self):
    #     print(type(Accessible_location.objects.all()))
    #     self.assertEqual(Accessible_location.objects.all(),(True or False))
    def test_test_dict(self):
        loc_list = [
            (40.68852572417966, -73.98657073016483),
            (40.68893870107474, -73.9863174112231),
        ]
        mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
        params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        allstr = True
        for loc in loc_list:
            url = mapbox_host + str(loc[1]) + "," + str(loc[0]) + ".json"
            response = requests.get(url=url, params=params).json()
            address = response["features"][0]["place_name"]
            address = " ".join(address.split(" ")[1:])
            allstr = allstr and (type(address) == str)
        self.assertEqual(allstr, True)


class LandingURLsTests(TestCase):
    def test_home_page(self):
        response = client.get("/home/")
        self.assertEqual(response.status_code, 200)

    def test_landing_page(self):
        response = client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_myFave_page(self):
        response = client.get("/myFav/")
        self.assertEqual(response.status_code, 302)

    def test_myFave_page_authenticated(self):
        user = User.objects.create(username="Testuser")
        client.force_login(user)
        response = client.get("/myFav/")
        self.assertEqual(response.status_code, 200)


class ViewsTests(TestCase):
    def test_views_index(self):
        response = client.get("/")
        self.assertEqual(response.resolver_match.func, landingpage)

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
            address="someaddress",
        )
        filteredLocations = Accessible_location.objects.all()

        cards = populate_cards(filteredLocations)
        # print(cards)
        # TODO: figure out why loaded cards dont seem to fit the location i created
        # Note: without infra_2 and accessible_location cards/addresses are empty strs
        self.assertNotEqual(cards, [])

    def test_lowVisionView(self):
        response = client.get(
            "/lowvision/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck=true&pol"
            "eCheck=true&sidewalkCheck=true&x-co=-74.0182495&y-co=40.6315015"
        )
        self.assertEqual(response.status_code, 200)

    def test_lowVisionView_no_params(self):
        response = client.get("/lowvision/")
        self.assertEqual(response.status_code, 200)

    def test_index_request(self):
        response = client.get(
            "/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck=true&pol"
            "eCheck=true&sidewalkCheck=true&x-co=-74.0182495&y-co=40.6315015"
        )
        self.assertEqual(response.status_code, 200)

    # def test_report_update_isAccessible(self):
    #     user = User.objects.create(username="Testuser")
    #     c = Client()
    #     c.force_login(user)
    #     infra_2 = Infra_type.objects.create(typeID=102)
    #     accessible_location = Accessible_location.objects.create(
    #         infraID=1111,
    #         locationX="st_1",
    #         locationY="st_2",
    #         typeID=infra_2,
    #         isAccessible=True,
    #         street1="street_1",
    #         street2="street_2",
    #         borough="Somewhere",
    #         address="someaddress",
    #     )
    #     post = {"infraID":1111, "comment":"broken"}
    #
    #     response = c.post("/report/", post, follow=True)
    #     # TODO: c.post not triggering if request.method == "POST"
    #     self.assertEqual(Accessible_location.isAccessible, False)
    # # TODO: test request.redirect_chain
    # # TODO: test comment was saved
    #
    # # TODO: test resolve report
    # # TODO: test isAccessible = True
    # # TODO: check redirect
    # # TODO: test report was deleted
    #
    # def test_add_favorite_authenticated(self):
    #     # TODO
    #     user = User.objects.create(username="Testuser")
    #     post = {"x_coord":-73.99244,
    #             "y_coord":40.72843,
    #             "address":"an address"}
    #     c = Client()
    #     c.force_login(user)
    #     self.assertEqual()
    #
    # def test_add_favorite_unauthenticated(self):
    #     # TODO
    #     pass
    #
    # def test_remove_favorite(self):
    #     #TODO
    #     pass
    #
    def test_go_to_favorites(self):
        # TODO
        pass


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
            address="someaddress",
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
            address="someaddress",
        )
        self.assertEqual(
            accessible_location.__str__(), "1111 st_1 st_2 infrastructure_type2 True"
        )

    def test_Favorite(self):
        user = User.objects.create(username="Testuser")
        favorite = Favorite.objects.create(
            userID=user,
            locationX="st_1",
            locationY="st_2",
            address="Empire State Building",
        )
        one_entry = Favorite.objects.get(
            userID=user,
            locationX="st_1",
            locationY="st_2",
            address="Empire State Building",
        )
        self.assertEqual(favorite, one_entry)
