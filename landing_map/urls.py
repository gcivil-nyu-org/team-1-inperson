from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("home/", views.index, name="home"),
    path("myFav/", views.myFav, name="myFav")
]
