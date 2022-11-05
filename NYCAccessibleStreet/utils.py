from decouple import config
from landing_map.models import Accessible_location, Infra_type
from report.models import Report
import requests


def test_dict():
    loc_list = [
        (40.68852572417966, -73.98657073016483),
        (40.68893870107474, -73.9863174112231),
    ]
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}

    for loc in loc_list:
        url = mapbox_host + str(loc[1]) + "," + str(loc[0]) + ".json"
        response = requests.get(url=url, params=params).json()
        address = response["features"][0]["place_name"]
        address = " ".join(address.split(" ")[1:])
        print("TEST DICT: ", address)


def get_locations():
    return Accessible_location.objects.all()


def populate_cards(locList):
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    # loc_list = [(40.68852572417966, -73.98657073016483), (40.68893870107474, -73.9863174112231)]
    # for loc in loc_list:
    # qset = Accessible_location.objects.filter()[:30]
    # print(qset)
    # q1 = Accessible_location(locationX = loc_list[0][1], \
    # locationY = loc_list[0][0], infraID = 1, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # q2 = Accessible_location(locationX = loc_list[1][1], \
    # locationY = loc_list[1][0], infraID = 2, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # qset = [q1,q2]
    # print(qset[0])
    # print(qset[1])
    # res = {}
    final = []
    for q in locList:
        card_info = {}
        # print(q)
        params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        url = mapbox_host + str(q.locationX) + "," + str(q.locationY) + ".json"
        response = requests.get(url=url, params=params).json()
        address = response["features"][0]["place_name"]
        # address = ' '.join(address.split(" ")[1:])

        # if card_info.get(address) is None:
        #     card_info[address] = {}

        #get report for each q
        try:
            report = Report.objects.get(infraID = q.infraID)
            comment = report.comment
            created = report.createdAt
            updated = report.updatedAt
        except:
            comment = ""
            created = ""
            updated = ""

        card_info["text"] = address
        card_info["type"] = str(q.typeID)
        card_info["card_id"] = q.infraID
        card_info["comment"] = comment
        card_info["time_reported"] = created
        card_info["last_update"] = updated
        # if str(q.typeID) == "Ramp":
        if q.isAccessible:
            card_info["isAccessible"] = True
        else:
            card_info["isAccessible"] = False
        # print(card_info)
        # print(cardList)
        final.append(card_info)
    # address_list = []
    # for card in cardList:
    #     address_list.append(card)
    # address_list = card.keys()
    return final


def populate_cards_by_address():
    cardList = []
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    # loc_list = [(40.68852572417966, -73.98657073016483), (40.68893870107474, -73.9863174112231)]
    # for loc in loc_list:
    qset = Accessible_location.objects.filter()[:30]
    # print(qset)
    # q1 = Accessible_location(locationX = loc_list[0][1], \
    # locationY = loc_list[0][0], infraID = 1, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # q2 = Accessible_location(locationX = loc_list[1][1], \
    # locationY = loc_list[1][0], infraID = 2, isAccessible = True, \
    # typeID = Infra_type.objects.get(typeName = "Ramp"))
    # qset = [q1,q2]
    # print(qset[0])
    # print(qset[1])
    card_id = 1
    card_info = {}
    # res = {}
    final = []
    address_set = set()

    for q in qset:
        # print(q)
        params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        url = mapbox_host + str(q.locationX) + "," + str(q.locationY) + ".json"
        response = requests.get(url=url, params=params).json()
        address = response["features"][0]["place_name"]
        address = " ".join(address.split(" ")[1:])
        if card_info.get(address) is None:
            card_info[address] = {}
        if str(q.typeID) == "Ramp":
            if q.isAccessible:
                # print("BEFORE UPDATE: ", card_info[address])
                # print("INSIDE IF: ", card_info[address].get("ramp_count"))
                card_info[address]["ramp_count"] = (
                    card_info[address].get("ramp_count", 0) + 1
                )
            else:
                card_info[address]["isRampAccess"] = False

        elif str(q.typeID) == "Signal":
            if q.isAccessible == "True":
                card_info[address]["signal_count"] = (
                    card_info[address].get("signal_count", 0) + 1
                )
            else:
                card_info[address]["isSignalAccess"] = False

        elif str(q.typeID) == "Raised_Crosswalk" and str(q.isAccessible):
            try:
                card_info[address]["rcross_count"] = (
                    card_info[address].get("rcross_count", 0) + 1
                )
            except KeyError:
                card_info[address]["rcross_count"] = 0

        try:
            if card_info[address]["signal_count"] is not None:
                pass
        except KeyError:
            card_info[address]["signal_count"] = 0

        try:
            if card_info[address]["ramp_count"] is not None:
                pass
        except KeyError:
            card_info[address]["ramp_count"] = 0

        try:
            if card_info[address]["rcross_count"] is not None:
                pass
        except KeyError:
            card_info[address]["rcross_count"] = 0

        try:
            if card_info[address]["isRampAccess"] is not None:
                pass
        except KeyError:
            card_info[address]["isRampAccess"] = True

        try:
            if card_info[address]["isSignalAccess"] is not None:
                pass
        except KeyError:
            card_info[address]["isSignalAccess"] = True

        if card_info[address].get("card_id") is None:
            card_info[address]["card_id"] = card_id
            card_id += 1
        # print(card_info)
        if address not in address_set:
            cardList.append(card_info)
            address_set.add(address)
    # print(cardList)
    # address_list = []
    # for card in cardList:
    #     address_list.append(card)
    # address_list = card.keys()
    for card, address in zip(cardList, address_set):
        res = {}
        print(address)
        res["text"] = address
        res["ramp_count"] = card[address]["ramp_count"]
        res["signal_count"] = card[address]["signal_count"]
        res["rcross_count"] = card[address]["rcross_count"]
        res["card_id"] = card[address]["card_id"]
        res["isRampAccess"] = card[address]["isRampAccess"]
        res["isSignalAccess"] = card[address]["isSignalAccess"]
        # print(res)
        final.append(res)
        print(final)

    return final
