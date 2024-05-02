from django.urls import path

from useradmin.views import (add_product, change_order_status, dashboard,
                             delete_product, edit_product, order_detail,
                             orders, products, reviews, settings, shop_page, change_password)

app_name = "useradmin"

urlpatterns = [
    path("dashboard/", dashboard, name="dashboard"),
    path("products/", products, name="products"),
    path("add-product/", add_product, name="add_product"),
    path("edit_product/<pid>/", edit_product, name="edit_product"),
    path("delete_product/<pid>/", delete_product, name="delete_product"),
    path("orders/", orders, name="orders"),
    path("order_detail/<id>/", order_detail, name="order_detail"),
    path('change_order_status/<id>/', change_order_status, name='change_order_status'),
    path("shop_page/", shop_page, name="shop_page"),
    path("reviews/", reviews, name="reviews"),
    path("settings/", settings, name="settings"),
    path("change_password/", change_password, name="change_password"),
]
