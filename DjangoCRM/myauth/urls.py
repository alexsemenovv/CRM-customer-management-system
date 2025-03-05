from django.contrib.auth.views import LoginView
from django.urls import path

from .views import (
    MyLogoutView,
    AboutMe,
)

app_name = "myauth"
urlpatterns = [
    path("login/", LoginView.as_view(
        template_name="myauth/login.html",
        redirect_authenticated_user=True,
    ), name="login"),
    path('logout/', MyLogoutView.as_view(), name='logout'),
    path('about-me/', AboutMe.as_view(), name='about_me'),
]
