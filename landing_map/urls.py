from django.urls import path
from . import views

urlpatterns = [
    path("", views.landingpage, name="landingpage"),
    path("home/", views.index, name="home"),
    path("report", views.report, name="report"),
    path("resolve_report", views.resolve_report, name="resolve_report"),
    path("myFav/", views.myFav, name="myFav"),
]
