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

    def test_infra_landing_map(self):
        temp = Infra_type.objects.create(typeID=102)
        accessible_location = Accessible_location.objects.create(
            infraID=1111,
            locationX="st_1",
            locationY="st_2",
            typeID=temp,
            isAccessible=True,
            street1="street_1",
            street2="street_2",
            borough="Somewhere",
        )
        entry = Accessible_location.objects.get(infraID=1111)
        self.assertEqual(entry, accessible_location)

    def test_index_request(self):
        r=client.get('/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck=true&poleCheck=true&sidewalkCheck=true&x-co=-74.0182495&y-co=40.6315015')



# def test_length_index(self):
    #     r=client.get('/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck=true&poleCheck=true&sidewalkCheck=true&x-co=-74.0182495&y-co=40.6315015')
    #     filterParams = r.GET
    #     print("filterparams", filterParams)
    #     print("request", request)
    #     print("request type", type(r))
    #     if filterParams.get("currentlyAccessible"):
    #         currentlyAccessible = []
    #         if filterParams.get("currentlyAccessible") == "true":
    #             currentlyAccessible.append(True)
    #         if filterParams.get("currentlyInaccessibleCheck") == "true":
    #             currentlyAccessible.append(False)
    #         else:
    #             currentlyAccessible.append(True)
    #
    #         infraTypes = []
    #         if filterParams.get("rampsCheck") == "true":
    #             infraTypes.append("1")
    #         if filterParams.get("poleCheck") == "true":
    #             infraTypes.append("2")
    #         if filterParams.get("sidewalkCheck") == "true":
    #             infraTypes.append("3")
    #
    #         radiusQuery = (
    #             "SELECT infraID, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) - radians({x}) ) "
    #             "+ sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location HAVING distance < "
    #             "{radius} ORDER BY distance".format(
    #                 y=filterParams.get("y-co"),
    #                 x=filterParams.get("x-co"),
    #                 radius=filterParams.get("radiusRange"),
    #             )
    #         )
    #
    #         infraIds = []
    #         nearbyLocations = Accessible_location.objects.raw(radiusQuery)
    #         for loc in nearbyLocations:
    #             infraIds.append(loc.infraID)
    #     else:
    #         radiusQuery = (
    #             "SELECT infraID, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) - radians({x}) ) "
    #             "+ sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location HAVING distance < "
    #             "{radius} ORDER BY distance".format(
    #                 y=40.68852572417966,
    #                 x=-73.98657073016483,
    #                 radius=1.0,
    #             )
    #         )
    #
    #         infraIds = []
    #         nearbyLocations = Accessible_location.objects.raw(radiusQuery)
    #         for loc in nearbyLocations:
    #             infraIds.append(loc.infraID)
    #     self.assertEqual(len(infraIds),len(nearbyLocations))



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
