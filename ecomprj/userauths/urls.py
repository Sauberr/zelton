from django.urls import path

from userauths.views import login, logout, profile_update, register

app_name = "userauths"

urlpatterns = [
    path("sign-up/", register, name="sign-up"),
    path("sign-in/", login, name="sign-in"),
    path("sign-out/", logout, name="sign-out"),
    path("profile/update/", profile_update, name="profile-update"),
]
