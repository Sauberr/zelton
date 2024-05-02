from django.urls import path

from userauths.views import (login_view, logout_view, profile_update,
                             register_view)

app_name = 'userauths'

urlpatterns = [
    path('sign-up/', register_view, name='sign-up'),
    path('sign-in/', login_view, name='sign-in'),
    path('sign-out/', logout_view, name='sign-out'),
    path('profile/update/', profile_update, name='profile-update')
]
