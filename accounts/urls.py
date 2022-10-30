from django.urls import path
from . import views
from .views import activate


urlpatterns = [
    path("signup/", views.register_page, name="signup"),
    path("login/", views.login_page, name="login"),
    path(
        r"activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/",
        activate,
        name="activate",
    ),
]
