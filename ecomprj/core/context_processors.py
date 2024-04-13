from django.contrib import messages
from django.db.models import Max, Min

from core.models import Address, Category, Product, Vendor, Wishlist


def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    products = Product.objects.all()

    min_max_price = Product.objects.aggregate(Min('price'), Max('price'))

    try:
        wishlist = Wishlist.objects.filter(user=request.user)
    except:
        messages.warning(request, "Please login first")
        wishlist = 0

    try:
        address = Address.objects.get(user=request.user)
    except:
        address = None
    return {'categories': categories, 'address': address, 'vendors': vendors, 'min_max_price': min_max_price, 'wishlist': wishlist, 'products': products}