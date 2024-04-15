from django.urls import path
from useradmin.views import dashboard

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
]