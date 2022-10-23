from django.shortcuts import render
from decouple import config
from .models import Infra_type, Favorite, Accessible_location
from django.core import serializers

def index(request):
    accessible_locations = serializers.serialize("json", Accessible_location.objects.all())
    context = {
        "mapboxAccessToken": config("MAPBOX_PUBLIC_TOKEN"),
        "accessible_locations": accessible_locations
    }
    return render(request, "landing_map/home.html", context)
