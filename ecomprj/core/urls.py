from django.urls import path
from core.views import (index, product_list_view, category_list_view, category_product_list_view, vendor_list_view,
        vendor_detail_view, product_detail_view, tag_list, ajax_add_review,
        search_view, filter_product, add_to_cart, cart_view, delete_item_from_cart, update_cart, checkout_view)

app_name = 'core'

urlpatterns = [

    path('', index, name='index'),
    path('products/', product_list_view, name='product-list'),
    path('product/<str:pid>/', product_detail_view, name='product-detail'),

    path('category/', category_list_view, name='category-list'),
    path('category/<str:cid>/', category_product_list_view, name='category-product-list'),

    path('vendors/', vendor_list_view, name='vendor-list'),
    path('vendor/<str:vid>/', vendor_detail_view, name='vendor-detail'),

    path('products/tag/<slug:tag_slug>/', tag_list, name='tags'),

    path('ajax-add-review/<str:pid>/', ajax_add_review, name='ajax-add-review'),

    path('search/', search_view, name='search'),

    path('filter-products/', filter_product, name='filter-products'),

    path('add-to-cart/', add_to_cart, name='add-to-cart'),
    path('cart/', cart_view, name='cart'),
    path("delete-from-cart/", delete_item_from_cart, name="delete-from-cart"),
    path('update-cart/', update_cart, name='update-cart'),

    path('checkout/', checkout_view, name='checkout'),

]
