from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("thesis_upload/", views.ThesisUploadPage, name="thesis_upload"),

    # Authentication
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]