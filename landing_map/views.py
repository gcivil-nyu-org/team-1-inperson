from django.shortcuts import render
from decouple import config
from .models import Infra_type, Favorite, Accessible_location
from django.core import serializers
import requests


def populate_cards():
    cardList = []
    mapbox_host = "https://api.mapbox.com/geocoding/v5/mapbox.places/"
    qset = Accessible_location.objects.filter()[:1]
    card_id = 1
    address_list = []

    for q in qset:
        res = {}
        params = {"access_token": config("MAPBOX_PUBLIC_TOKEN"), "types": "address"}
        url = mapbox_host + str(q.locationX) + "," + str(q.locationY) + ".json"
        response = requests.get(url=url, params=params).json()
        card_info = {}
        address = response["features"][0]["place_name"]
        address_list.append(address)
        card_info[address] = {}
        if str(q).split(" ")[-2] == "Ramp":
            if str(q).split(" ")[-1] == "True":
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

        res["text"] = address
        res["ramp_count"] = card_info[address]["ramp_count"]
        res["signal_count"] = card_info[address]["signal_count"]
        res["rcross_count"] = card_info[address]["rcross_count"]
        res["card_id"] = card_info[address]["card_id"]
        res["isRampAccess"] = card_info[address]["isRampAccess"]
        res["isSignalAccess"] = card_info[address]["isSignalAccess"]
        cardList.append(res)

    return cardList, address_list


def index(request):

    filterParams = request.GET

    if filterParams.get("currentlyAccessible"):
        currentlyAccessible = []
        if filterParams.get("currentlyAccessible") == "true":
            currentlyAccessible.append(True)
        if filterParams.get("currentlyInaccessibleCheck") == "true":
            currentlyAccessible.append(False)
        else:
            currentlyAccessible.append(True)

        infraTypes = []
        if filterParams.get("rampsCheck") == "true":
            infraTypes.append("1")
        if filterParams.get("poleCheck") == "true":
            infraTypes.append("2")
        if filterParams.get("sidewalkCheck") == "true":
            infraTypes.append("3")

        radiusQuery = "SELECT infraID, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) - radians({x}) ) " \
                      "+ sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location HAVING distance < " \
                      "{radius} ORDER BY distance".format(y = filterParams.get("y-co"), x= filterParams.get("x-co"), radius = filterParams.get("radiusRange") )

        infraIds = []
        nearbyLocations = Accessible_location.objects.raw(radiusQuery)
        for loc in nearbyLocations:
            infraIds.append(loc.infraID)

        filteredLocations = Accessible_location.objects.filter(infraID__in=infraIds,isAccessible__in=currentlyAccessible, typeID__in=infraTypes)
    else:
        filteredLocations = Accessible_location.objects.all()
    cardList, address_list = populate_cards()
    accessible_locations = serializers.serialize("json", filteredLocations)

    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": accessible_locations,
        "cardList": cardList,
    }
    return render(request, "landing_map/home.html", context)
