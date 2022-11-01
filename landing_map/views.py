from django.shortcuts import render
from decouple import config
from .models import Infra_type, Favorite, Accessible_location
from django.core import serializers
from NYCAccessibleStreet.utils import (
    get_locations,
    populate_cards_by_address,
    populate_cards_individual,
)


def index(request):
    cardList = populate_cards()
    accessible_locations = serializers.serialize(
        "json", Accessible_location.objects.all()
    )

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

        radiusQuery = (
            "SELECT infraID, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) - radians({x}) ) "
            "+ sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location HAVING distance < "
            "{radius} ORDER BY distance".format(
                y=filterParams.get("y-co"),
                x=filterParams.get("x-co"),
                radius=filterParams.get("radiusRange"),
            )
        )

        infraIds = []
        nearbyLocations = Accessible_location.objects.raw(radiusQuery)
        for loc in nearbyLocations:
            infraIds.append(loc.infraID)

        filteredLocations = Accessible_location.objects.filter(
            infraID__in=infraIds,
            isAccessible__in=currentlyAccessible,
            typeID__in=infraTypes,
        )
    else:
        filteredLocations = Accessible_location.objects.all()
    cardList = populate_cards_individual(filteredLocations)
    # print(cardList)
    accessible_locations = serializers.serialize("json", filteredLocations)

    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": accessible_locations,
        "cardList": cardList,
    }
    return render(request, "landing_map/home.html", context)
