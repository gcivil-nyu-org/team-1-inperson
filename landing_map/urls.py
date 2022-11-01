from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("home/", views.index, name="home"),
]
