from decouple import config
from landing_map.models import Accessible_location
import requests

def test_dict():
    loc_list = [(40.68852572417966, -73.98657073016483), (40.68893870107474, -73.9863174112231)]
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}

    for loc in loc_list:
        url = mapbox_host + str(loc[1]) + "," + str(loc[0]) + ".json"
        response = requests.get(url=url, params=params).json()
        address = response["features"][0]["place_name"]
        address = ' '.join(address.split(" ")[1:])
        print("TEST DICT: ", address)

def populate_cards():
    cardList = []
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    qset = Accessible_location.objects.filter()[:30]
    # loc_list = [(40.68852572417966, -73.98657073016483), (40.68893870107474, -73.9863174112231)]
    card_id = 1
    card_info = {}
    # res = {}
    final = []
    address_set = set()

    for q in (qset):
        params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        url = mapbox_host + str(q.locationX) + "," + str(q.locationY) + ".json"
        response = requests.get(url=url, params=params).json()
        address = response["features"][0]["place_name"]
        address = ' '.join(address.split(" ")[1:])
        if card_info.get(address) is None:
            card_info[address] = {}
        if str(q).split(" ")[-2] == "Ramp":
            if str(q).split(" ")[-1] == "True":
                # print("BEFORE UPDATE: ", card_info[address])
                # print("INSIDE IF: ", card_info[address].get("ramp_count"))
                card_info[address]["ramp_count"] = (
                    card_info[address].get("ramp_count", 0) + 1
                )
            else:
                card_info[address]["isRampAccess"] = False

        elif str(q).split(" ")[-2] == "Signal":
            if str(q).split(" ")[-1] == "True":
                card_info[address]["signal_count"] = (
                    card_info[address].get("signal_count", 0) + 1
                )
            else:
                card_info[address]["isSignalAccess"] = False

        elif (
            str(q).split(" ")[-2] == "Raised_Crosswalk"
            and str(q).split(" ")[-1] == "True"
        ):
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
    for card,address in zip(cardList, address_set):
        res = {}
        # print(address)
        res["text"] = address
        res["ramp_count"] = card[address]["ramp_count"]
        res["signal_count"] = card[address]["signal_count"]
        res["rcross_count"] = card[address]["rcross_count"]
        res["card_id"] = card[address]["card_id"]
        res["isRampAccess"] = card[address]["isRampAccess"]
        res["isSignalAccess"] = card[address]["isSignalAccess"]
        # print(res)
        final.append(res)
        # print(final)

    return final