from django.urls import path
from . import views

urlpatterns = [
    path('', views.mainmap, name='mainmap'),
]