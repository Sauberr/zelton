from django.urls import path
from useradmin.views import dashboard, products, add_product

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("products/", products, name="products"),
    path("add-product/", add_product, name="add_product"),
]