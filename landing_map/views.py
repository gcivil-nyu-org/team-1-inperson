from django.shortcuts import render, redirect
from decouple import config
from .models import Favorite, Accessible_location
from report.models import Report
from django.core import serializers
from django.http import HttpResponse
from NYCAccessibleStreet.utils import (
    populate_cards,
    getAddressFromMapbox,
    populate_favorite_cards,
)


def index(request):
    loggedIn = False
    if request.user.is_authenticated:
        loggedIn = True
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
                radius=1.0,
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
    accessible_locations = serializers.serialize("json", filteredLocations)

    # x and y for favorites
    y = filterParams.get("y-co")
    x = filterParams.get("x-co")
    # check if current address is favorited already
    favorited = False
    if request.user.is_authenticated:
        if Favorite.objects.filter(userID=request.user, address=locationAddress):
            favorited = True

    favPage = False
    if filterParams.get("favPage"):
        favPage = True

    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": accessible_locations,
        "cardList": cardList,
        "locationAddress": locationAddress,
        "x_coord": x,
        "y_coord": y,
        "favorited": favorited,
        "hideSearchBar": favPage,
        "loggedIn": loggedIn,
    }
    return render(request, "landing_map/home.html", context)


def lowVisionView(request):
    loggedIn = False
    if request.user.is_authenticated:
        loggedIn = True
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

    # x and y for favorites
    y = filterParams.get("y-co")
    x = filterParams.get("x-co")
    # check if current address is favorited already
    favorited = False
    if request.user.is_authenticated:
        if Favorite.objects.filter(userID=request.user, address=locationAddress):
            favorited = True

    favPage = False
    if filterParams.get("favPage"):
        favPage = True

    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": filteredLocations,
        "cardList": cardList,
        "locationAddress": locationAddress,
        "x_coord": x,
        "y_coord": y,
        "favorited": favorited,
        "hideSearchBar": favPage,
        "loggedIn": loggedIn,
    }
    return render(request, "landing_map/lowVisionView.html", context)


def landingpage(request):
    context = {"mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN")}
    return render(request, "landing_map/landingpage.html", context)


def myFav(request):
    if request.user.is_authenticated:
        user_favorites = Favorite.objects.filter(userID=request.user)
        favorite_card_list = populate_favorite_cards(user_favorites)
        context = {
            "favorite_card_list": favorite_card_list,
            "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        }
        return render(request, "landing_map/myFav.html", context)
    else:
        return redirect("login")


def report(request):
    if request.user.is_authenticated:
        if request.method == "POST":

            x = request.POST.get("x_coord")
            y = request.POST.get("y_coord")

            infra = request.POST.get("infraID")
            obj = Accessible_location.objects.get(pk=infra)
            # Hopefully stops multiple reports from being saved, Probably need better solution
            if not obj.isAccessible:
                return HttpResponse("Report already made! Please reload")
            obj.isAccessible = False
            obj.save()
            inComment = request.POST.get("comment")
            newReport = Report(user=request.user, infraID=obj, comment=inComment)
            newReport.save()

            pageURL = (
                "/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck="
                "true&poleCheck=true&sidewalkCheck=true&x-co={x}&y-co={y}".format(
                    x=x, y=y
                )
            )

        return redirect(pageURL)
    else:
        return redirect("login")


def resolve_report(request):
    if request.user.is_authenticated:

        x = request.POST.get("x_coord")
        y = request.POST.get("y_coord")

        infra = request.POST.get("infraID")
        locObj = Accessible_location.objects.get(pk=infra)
        locObj.isAccessible = True
        locObj.save()
        Report.objects.get(infraID=infra).delete()

        pageURL = (
            "/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck="
            "true&poleCheck=true&sidewalkCheck=true&x-co={x}&y-co={y}".format(x=x, y=y)
        )

        return redirect(pageURL)
    else:
        return redirect("login")


def add_favorite(request):
    if not request.user.is_authenticated:
        return redirect("login")
    x = request.POST.get("x_coord")
    y = request.POST.get("y_coord")
    address = request.POST.get("address")
    newFav = Favorite(userID=request.user, locationX=x, locationY=y, address=address)
    newFav.save()

    pageURL = (
        "/home/?radiusRange=2.75&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck="
        "true&poleCheck=true&sidewalkCheck=true&x-co={x}&y-co={y}".format(x=x, y=y)
    )
    return redirect(pageURL)


def remove_favorite(request):
    x = request.POST.get("x")
    y = request.POST.get("y")
    address = request.POST.get("address")
    Favorite.objects.get(
        userID=request.user, address=address, locationX=x, locationY=y
    ).delete()
    return redirect("/myFav")


def goto_favorite(request):
    x = request.POST.get("x")
    y = request.POST.get("y")
    pageURL = (
        "/home/?radiusRange=0.5&currentlyAccessible=true&currentlyInaccessibleCheck=true&rampsCheck="
        "true&poleCheck=true&sidewalkCheck=true&x-co={x}&y-co={y}&favPage=true".format(
            x=x, y=y
        )
    )
    return redirect(pageURL)
