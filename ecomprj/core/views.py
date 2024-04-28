import calendar

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.db.models import Avg, Count
from django.db.models.functions import ExtractMonth
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from taggit.models import Tag

from core.forms import ProductReviewForm
from core.models import (Address, CartOrder, CartOrderProducts, Category,
                         Product, ProductReview, Vendor, Wishlist, Coupon)
from userauths.models import ContactUs, Profile

import stripe

from django.conf import settings


def index(request):
    products = Product.objects.filter(product_status='published', featured=True).order_by('-id')

    context = {'products': products, 'title': 'Home'}
    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status='published')
    tags = Tag.objects.all()
    context = {'products': products, 'title': 'Products', 'tags': tags}
    return render(request, 'core/product-list.html', context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    review_form = ProductReviewForm()
    make_review = True
    if request.user.is_authenticated:
        user_review_count = ProductReview.objects.filter(user=request.user, product=product).count()
        if user_review_count > 0:
            make_review = False
    context = {'p': product, 'p_image': p_image, 'products': products, 'reviews': reviews, 'average_rating': average_rating, 'review_form': review_form, 'make_review': make_review, 'title': product.title}
    return render(request, 'core/product-detail.html', context)


def category_list_view(request):
    # categories = Category.objects.all().annotate(product_count=Count('category'))
    categories = Category.objects.all()
    context = {'categories': categories, 'title': 'Categories'}
    return render(request, 'core/category-list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)
    context = {'category': category, 'products': products, 'title': category.title}
    return render(request, 'core/category-product-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {'vendors': vendors, 'title': 'Vendors'}
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published')
    context = {'vendor': vendor, 'products': products, 'title': vendor.title}
    return render(request, 'core/vendor-detail.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {'products': products, 'tag': tag, 'title': 'Tags'}
    return render(request, 'core/tag.html', context)


def ajax_add_review(request, pid):
    product = Product.objects.get(pid=pid)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review=request.POST['review'],
        rating=request.POST['rating']
    )
    context = {
        'user': user.username,
        'review': request.POST['review'],
        'rating': request.POST['rating'],
        'title': 'Review',
    }
    average_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    return JsonResponse(
        {
            'bool': True,
            'context': context,
            'average_reviews': average_reviews
        }
    )


def search_view(request):
    query = request.GET.get('q')
    products = Product.objects.filter(title__icontains=query).order_by('-date')
    context = {'products': products, 'query': query, 'title': 'Search'}
    return render(request, 'core/search.html', context)


def filter_product(request):
    categories = request.GET.getlist('category[]')
    vendors = request.GET.getlist('vendor[]')

    min_price = request.GET['min_price']
    max_price = request.GET['max_price']

    products = Product.objects.filter(product_status='published').order_by('-id').distinct()

    products = products.filter(price__gte=min_price)
    products = products.filter(price__lte=max_price)

    if len(categories) > 0:
        products = products.filter(category__id__in=categories).distinct()

    if len(vendors) > 0:
        products = products.filter(vendor__id__in=vendors).distinct()

    data = render_to_string('core/async/product-list.html', {'products': products, 'title': 'Filtered Products'})
    return JsonResponse({'data': data})


def add_to_cart(request):
    cart_product = {}

    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'pid': request.GET['pid'],
    }

    if 'cart_data_obj' in request.session:
        if str(request.GET['id']) in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)
            request.session['cart_data_obj'] = cart_data
        else:
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        request.session['cart_data_obj'] = cart_product
    return JsonResponse({'data': request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj'])})


def cart_view(request):
    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])
        return render(request, "core/cart.html", {"cart_data": request.session['cart_data_obj'], 'totalcartitems': len(request.session['cart_data_obj']), 'cart_total_amount': cart_total_amount, 'title': 'Cart'})
    else:
        messages.warning(request, "Your cart is empty")
        return redirect("core:index")


def delete_item_from_cart(request):
    product_id = str(request.GET['id'])
    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            del request.session['cart_data_obj'][product_id]
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'],
                                                             'totalcartitems': len(request.session['cart_data_obj']),
                                                             'cart_total_amount': cart_total_amount, 'title': 'Cart'})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def update_cart(request):
    product_id = str(request.GET['id'])
    product_qty = request.GET['qty']

    if 'cart_data_obj' in request.session:
        if product_id in request.session['cart_data_obj']:
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    cart_total_amount = 0
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item['qty']) * float(item['price'])

    context = render_to_string("core/async/cart-list.html", {"cart_data": request.session['cart_data_obj'],
                                                             'totalcartitems': len(request.session['cart_data_obj']),
                                                             'cart_total_amount': cart_total_amount, 'title': 'Cart'})
    return JsonResponse({"data": context, 'totalcartitems': len(request.session['cart_data_obj'])})


def save_checkout_info(request):
    cart_total_amount = 0
    total_amount = 0

    if request.method == "POST":
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')
        city = request.POST.get('city')
        state = request.POST.get('state')
        country = request.POST.get('country')

        request.session['full_name'] = full_name
        request.session['email'] = email
        request.session['address'] = address
        request.session['mobile'] = mobile
        request.session['city'] = city
        request.session['state'] = state
        request.session['country'] = country

        # Checking if cart_data_obj session exists
        if 'cart_data_obj' in request.session:
            # Getting total amount for Paypal amount
            for p_id, item in request.session['cart_data_obj'].items():
                total_amount += int(item['qty']) * float(item['price'])

            full_name = request.session['full_name']
            email = request.session['email']
            phone = request.session['mobile']
            address = request.session['address']
            city = request.session['city']
            state = request.session['state']
            country = request.session['country']

            # Create order object
            order = CartOrder.objects.create(
                user=request.user,
                price=total_amount,
                full_name=full_name,
                email=email,
                address=address,
                phone=phone,
                city=city,
                state=state,
                country=country,
            )

            del request.session['full_name']
            del request.session['email']
            del request.session['address']
            del request.session['mobile']
            del request.session['city']
            del request.session['state']
            del request.session['country']

            # Getting total amount for the cart
            for p_id, item in request.session['cart_data_obj'].items():
                cart_total_amount += int(item['qty']) * float(item['price'])

                cart_order_products = CartOrderProducts.objects.create(
                    order=order,
                    invoice_no='INVOICE_NO-' + str(order.id),
                    item=item['title'],
                    image=item['image'],
                    qty=item['qty'],
                    price=item['price'],
                    total=float(item['qty']) * float(item['price'])
                )
        return redirect('core:checkout', order.oid)
    return redirect('core:checkout', order.oid)


def checkout(request, oid):
    order = CartOrder.objects.get(oid=oid)
    order_items = CartOrderProducts.objects.filter(order=order)

    if request.method == 'POST':
        code = request.POST.get('code')
        coupon = Coupon.objects.filter(code=code, active=True).first()
        if coupon:
            if coupon in order.coupons.all():
                messages.warning(request, 'Coupon already used')
                return redirect('core:checkout', order.oid)
            else:
                discount = order.price * coupon.discount / 100
                order.coupons.add(coupon)
                order.price -= discount
                order.saved += discount
                order.save()
                messages.success(request, 'Coupon ACTIVATED')
                return redirect('core:checkout', order.oid)
        else:
            messages.warning(request, 'Invalid Coupon')
            return redirect('core:checkout', order.oid)

    context = {'order': order, 'order_items': order_items, 'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY, 'title': 'Checkout'}
    return render(request, 'core/checkout.html', context)


@csrf_exempt
def create_checkout_session(request, oid):
    order = CartOrder.objects.get(oid=oid)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        customer_email=order.email,
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'USD',
                    'product_data': {
                        'name': order.full_name,
                    },
                    'unit_amount': int(order.price * 1000)
                },
                'quantity': 1
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('core:payment-completed', args=[order.oid])) + '?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('core:payment-failed'))
    )

    order.paid_status = False
    order.stripe_payment_intent = checkout_session['id']
    order.save()

    return JsonResponse({'sessionId': checkout_session['id']})


@login_required
def payment_details(request, oid):
    order = CartOrder.objects.get(oid=oid)
    cart_total = 0
    if 'cart_data_obj' in request.session:
        for product_id, item in request.session['cart_data_obj'].items():
            cart_total += float(item['price']) * int(item['qty'])
    cart_total -= float(order.saved)
    context = {
        'order': order,
        'cart_data': request.session['cart_data_obj'],
        'totalcartitems': len(request.session['cart_data_obj']),
        'cart_total': cart_total,
        'saved': order.saved,
        'title': 'Payment Details',
    }
    return render(request, 'core/payment-details.html', context)


@login_required
def payment_completed_view(request, oid):
    order = CartOrder.objects.get(oid=oid)
    if order.paid_status == False:
        order.paid_status = True
        order.save()

    context = {'order': order, 'title': 'Payment Completed'}
    return render(request, 'core/payment-completed.html', context)


@login_required
def payment_failed_view(request):
    context = {'title': 'Payment Failed'}
    return render(request, 'core/payment-failed.html', context)


@login_required
def customer_dashboard(request):
    order_list = CartOrder.objects.filter(user=request.user).order_by('-id')
    address = Address.objects.filter(user=request.user)

    profile = Profile.objects.get(user=request.user)

    orders = CartOrder.objects.annotate(month=ExtractMonth('order_date')).values('month').annotate(count=Count('id')).values('month', 'count')
    month = []
    total_orders = []

    for i in orders:
        month.append(calendar.month_name[i['month']])
        total_orders.append(i['count'])

    if request.method == 'POST':
        address = request.POST.get('address')
        mobile = request.POST.get('mobile')

        new_address = Address.objects.create(
            user=request.user,
            address=address,
            mobile=mobile,
        )
        messages.success(request, 'Address has been added successfully')
        return redirect('core:dashboard')

    context = {
        'profile': profile,
        'order_list': order_list,
        'address': address,
        'orders': orders,
        'month': month,
        'total_orders': total_orders,
        'title': 'Dashboard',
    }
    return render(request, 'core/dashboard.html', context)


@login_required
def order_detail(request, id):
    order = CartOrder.objects.get(user=request.user, id=id)
    order_items = CartOrderProducts.objects.filter(order=order)
    context = {
        'order_items': order_items,
        'title': 'Order Detail',
    }
    return render(request, 'core/order-detail.html', context)


def make_address_default(request):
    id = request.GET['id']
    Address.objects.update(status=False)
    Address.objects.filter(id=id).update(status=True)
    return JsonResponse({'boolean': True})


@login_required
def wishlist_view(request):
    try:
        wishlist = Wishlist.objects.all()
    except:
        wishlist = None
    context = {'w': wishlist, 'title': 'Wishlist'}
    return render(request, 'core/wishlist.html', context)


def add_to_wishlist(request):
    product_id = request.GET['id']
    product = Product.objects.get(id=product_id)

    wishlist_count = Wishlist.objects.filter(product=product, user=request.user).count()
    print(wishlist_count)

    if wishlist_count > 0:
        context = {
            "bool": True
        }
    else:
        new_wishlist = Wishlist.objects.create(
            user=request.user,
            product=product,
        )
        context = {
            "bool": True,
            'title': 'Wishlist',
        }

    return JsonResponse(context)


def remove_wishlist(request):
    pid = request.GET['id']
    wishlist = Wishlist.objects.filter(user=request.user)

    wishlist_id = Wishlist.objects.get(id=pid)
    delete_product = wishlist_id.delete()

    context = {
        "bool": True,
        "w": wishlist,
        'title': 'Wishlist',
    }
    wishlist_json = serializers.serialize('json', wishlist)
    data = render_to_string("core/async/wishlist-list.html", context)
    return JsonResponse({"data": data, "w": wishlist_json})


def contact(request):
    context = {'title': 'Contact Us'}
    return render(request, 'core/contact.html', context)


def ajax_contact_form(request):
    full_name = request.GET['full_name']
    email = request.GET['email']
    phone = request.GET['phone']
    subject = request.GET['subject']
    message = request.GET['message']

    contact = ContactUs.objects.create(
        full_name=full_name,
        email=email,
        phone=phone,
        subject=subject,
        message=message,
    )

    data = {'bool': True, 'message': 'Message sent successfully'}

    return JsonResponse({'data': data, 'title': 'Contact Us'})








