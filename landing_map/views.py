from django.shortcuts import render, redirect
from decouple import config
from .models import Infra_type, Favorite, Accessible_location
from report.models import Report
from .forms import ReportForm
from django.core import serializers
from NYCAccessibleStreet.utils import populate_cards, getAddressFromMapbox


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
        radiusQuery = (
            "SELECT infraID, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) - radians({x}) ) "
            "+ sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location HAVING distance < "
            "{radius} ORDER BY distance".format(
                y=40.68852572417966,
                x=-73.98657073016483,
                radius=1.0,
            )
        )

        infraIds = []
        nearbyLocations = Accessible_location.objects.raw(radiusQuery)
        for loc in nearbyLocations:
            infraIds.append(loc.infraID)
        filteredLocations = Accessible_location.objects.filter(
            infraID__in=infraIds,
            isAccessible__in=[True, False],
            typeID__in=["1", "2", "3"],
        )
    cardList = populate_cards(filteredLocations)
    accessible_locations = serializers.serialize("json", filteredLocations)

    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": accessible_locations,
        "cardList": cardList,
    }
    return render(request, "landing_map/home.html", context)


def lowVisionView(request):
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
        locationAddress = getAddressFromMapbox(
            filterParams.get("x-co"), filterParams.get("y-co")
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
        radiusQuery = (
            "SELECT infraID, ( 3959 * acos( cos( radians({y}) ) * cos( radians(locationY) ) * cos( radians(locationX) - radians({x}) ) "
            "+ sin( radians({y}) ) * sin(radians(locationY)) ) ) AS distance FROM landing_map_accessible_location HAVING distance < "
            "{radius} ORDER BY distance".format(
                y=40.68852572417966,
                x=-73.98657073016483,
                radius=2.75,
            )
        )
        locationAddress = getAddressFromMapbox(-73.98657073016483, 40.68852572417966)

        infraIds = []
        nearbyLocations = Accessible_location.objects.raw(radiusQuery)
        for loc in nearbyLocations:
            infraIds.append(loc.infraID)
        filteredLocations = Accessible_location.objects.filter(
            infraID__in=infraIds,
            isAccessible__in=[True, False],
            typeID__in=["1", "2", "3"],
        )
    cardList = populate_cards(filteredLocations)

    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": filteredLocations,
        "cardList": cardList,
        "locationAddress": locationAddress,
    }
    return render(request, "landing_map/lowVisionView.html", context)


def landingpage(request):
    return render(request, "landing_map/landingpage.html", {})


def myFav(request):
    return render(request, "landing_map/myFav.html", {})


def report(request):
    if request.method == "POST":
        print("post")
        infra = request.POST.get("infraID")
        obj = Accessible_location.objects.get(pk=infra)
        obj.isAccessible = False
        obj.save()
        inComment = request.POST.get("comment")
        newReport = Report(user=request.user, infraID=obj, comment=inComment)
        newReport.save()

    return redirect("home")


def resolve_report(request):
    infra = request.POST.get("infraID")
    locObj = Accessible_location.objects.get(pk=infra)
    locObj.isAccessible = True
    locObj.save()
    Report.objects.get(infraID=infra).delete()

    return redirect("home")
