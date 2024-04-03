from django.urls import path, include
from core.views import (index, product_list_view, category_list_view, category_product_list_view, vendor_list_view,
        vendor_detail_view, product_detail_view, tag_list, ajax_add_review, search_view, filter_product, add_to_cart,
        cart_view, delete_item_from_cart, update_cart, checkout_view, payment_completed_view,
        payment_failed_view, customer_dashboard, order_detail)

app_name = 'core'

urlpatterns = [
    # Homepage
    path('', index, name='index'),
    path('products/', product_list_view, name='product-list'),
    path('product/<str:pid>/', product_detail_view, name='product-detail'),

    # Category
    path('category/', category_list_view, name='category-list'),
    path('category/<str:cid>/', category_product_list_view, name='category-product-list'),

    # Vendor
    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<str:vid>/', vendor_detail_view, name='vendor-detail'),

    # Tags
    path('products/tag/<slug:tag_slug>/', tag_list, name='tags'),

    # Reviews
    path('ajax-add-review/<str:pid>/', ajax_add_review, name='ajax-add-review'),

    # Search
    path('search/', search_view, name='search'),

    # Filter product
    path('filter-products/', filter_product, name='filter-products'),

    # Cart
    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_view, name='cart'),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path('update-cart/', update_cart, name='update-cart'),

    # Checkout
    path('checkout/', checkout_view, name='checkout'),

    # Paypal
    path('paypal/', include('paypal.standard.ipn.urls')),

    # Payment Successful
    path('payment-completed/', payment_completed_view, name='payment-completed'),

    # Payment Failed
    path('payment-failed/', payment_failed_view, name='payment-failed'),

    # Dashboard
    path('dashboard/', customer_dashboard, name='dashboard'),

    # Order detail
    path('dashboard/order/<int:id>/', order_detail, name='order-detail'),

]
