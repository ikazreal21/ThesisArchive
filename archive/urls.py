from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    path("", views.Home, name="home"),
    path("thesis_upload/", views.ThesisUploadPage, name="thesis_upload"),
    path("myuploads/", views.MyUploads, name="myuploads"),
    path("profile/", views.ProfilePage, name="profile"),
    path("compare/", views.CompareResearch, name="compare"),

    # Authentication
    path("password_change/", views.ChangePassword, name="password_change"),
    path("register/", views.Register, name="register"),
    path("login/", views.Login, name="login"),
    path("logout/", views.Logout, name="logout"),
]