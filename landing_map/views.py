from django.shortcuts import render
from decouple import config


def index(request):
    context = {"mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN")}
    return render(request, "landing_map/home.html", context)
