from django.urls import include, path

from core.views import (add_to_cart, add_to_wishlist, ajax_add_review,
                        ajax_contact_form, cart, category_list,
                        category_product_list, checkout, contact,
                        create_checkout_session, customer_dashboard,
                        delete_item_from_cart, filter_product, index,
                        make_address_default, order_detail, payment_completed,
                        payment_details, payment_failed, product_detail,
                        product_list, remove_wishlist, save_checkout_info,
                        search, tag_list, update_cart, vendor_detail,
                        vendor_list, wishlist)

app_name = "core"

urlpatterns = [
    # Homepage
    path("", index, name="index"),
    path("products/", product_list, name="product-list"),
    path("product/<str:pid>/", product_detail, name="product-detail"),
    # Category
    path("category/", category_list, name="category-list"),
    path(
        "category/<str:cid>/", category_product_list, name="category-product-list"
    ),
    # Vendor
    path("vendors/", vendor_list, name="vendor-list"),
    path("vendor/<str:vid>/", vendor_detail, name="vendor-detail"),
    # Tags
    path("products/tag/<slug:tag_slug>/", tag_list, name="tags"),
    # Reviews
    path("ajax-add-review/<str:pid>/", ajax_add_review, name="ajax-add-review"),
    # Search
    path("search/", search, name="search"),
    # Filter product
    path("filter-products/", filter_product, name="filter-products"),
    # Cart
    path("add-to-cart/", add_to_cart, name="add-to-cart"),
    path("cart/", cart, name="cart"),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path("update-cart/", update_cart, name="update-cart"),
    # Checkout
    path("checkout/<str:oid>/", checkout, name="checkout"),
    path("save_checkout_info/", save_checkout_info, name="save_checkout_info"),
    # Paypal
    path("paypal/", include("paypal.standard.ipn.urls")),
    # Payment Successful
    path("payment-completed/<oid>/", payment_completed, name="payment-completed"),
    path("payment-details/<oid>/", payment_details, name="payment-details"),
    # Payment Failed
    path("payment-failed/", payment_failed, name="payment-failed"),
    # Dashboard
    path("dashboard/", customer_dashboard, name="dashboard"),
    # Order detail
    path("dashboard/order/<int:id>/", order_detail, name="order-detail"),
    # Making address default
    path("make-default-address/", make_address_default, name="make-default-address"),
    # Wishlist
    path("wishlist/", wishlist, name="wishlist"),
    # Add to wishlist
    path("add-to-wishlist/", add_to_wishlist, name="add-to-wishlist"),
    # Remove from wishlist
    path("remove-from-wishlist/", remove_wishlist, name="remove-from-wishlist"),
    # Contact
    path("contact/", contact, name="contact"),
    path("ajax-contact-form/", ajax_contact_form, name="ajax-contact-form"),
    path(
        "api/create_checkout_session/<oid>/",
        create_checkout_session,
        name="create_checkout_session",
    ),
]
