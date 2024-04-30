import datetime

from django.contrib import messages
from django.db.models import Sum
from django.shortcuts import redirect, render

from core.models import (CartOrder, CartOrderProducts, Category, Product,
                         ProductReview)
from useradmin.forms import AddProductForm
from userauths.models import Profile, User


def dashboard(request):
    revenue = CartOrder.objects.aggregate(price=Sum("price"))
    total_orders_count = CartOrder.objects.all()
    all_products = Product.objects.all()
    all_categories = Category.objects.all()
    new_customers = User.objects.all().order_by("-id")
    latest_orders = CartOrder.objects.all()

    this_month = datetime.datetime.now().month

    monthly_revenue = CartOrder.objects.filter(order_date__month=this_month).aggregate(price=Sum("price"))

    context = {
        "revenue": revenue,
        "total_orders_count": total_orders_count,
        "all_products": all_products,
        "all_categories": all_categories,
        "new_customers": new_customers,
        "latest_orders": latest_orders,
        "monthly_revenue": monthly_revenue,
        "title": "Admin Dashboard",
    }

    return render(request, 'useradmin/dashboard.html', context)


def products(request):
    all_products = Product.objects.all()
    all_categories = Category.objects.all()

    context = {
        "all_products": all_products,
        "all_categories": all_categories,
        "title": "Products",
    }

    return render(request, 'useradmin/products.html', context)


def add_product(request):
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:products')
    else:
        form = AddProductForm()

    context = {
        "form": form,
        "title": "Add Product",
    }

    return render(request, 'useradmin/add-product.html', context)


def edit_product(request, pid):
    product = Product.objects.get(pid=pid)
    if request.method == 'POST':
        form = AddProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.user = request.user
            new_form.save()
            form.save_m2m()
            return redirect('useradmin:edit_product', product.pid)
    else:
        form = AddProductForm(instance=product)

    context = {
        "form": form,
        "title": "Edit Product",
        "product": product,
    }

    return render(request, 'useradmin/edit-product.html', context)


def delete_product(request, pid):
    product = Product.objects.get(pid=pid)
    product.delete()
    return redirect('useradmin:products')


def orders(request):
    orders = CartOrder.objects.all()

    context = {
        "orders": orders,
        "title": "Orders",
    }

    return render(request, 'useradmin/orders.html', context)


def order_detail(request, id):
    order = CartOrder.objects.get(id=id)
    order_items = CartOrderProducts.objects.filter(order=order)

    context = {
        "order": order,
        "order_items": order_items,
        "title": "Order Detail",
    }

    return render(request, 'useradmin/order_detail.html', context)


def change_order_status(request, id):
    order = CartOrder.objects.get(id=id)
    if request.method == 'POST':
        status = request.POST.get('status')
        order.product_status = status
        order.save()
        messages.success(request, f'Order status change to {status}')

    return redirect('useradmin:order_detail', order.id)


def shop_page(request):
    products = Product.objects.all()
    revenue = CartOrder.objects.aggregate(price=Sum('price'))
    total_sales = CartOrderProducts.objects.filter(order__paid_status=True).aggregate(qty=Sum('qty'))
    context = {
        "products": products,
        "revenue": revenue,
        "total_sales": total_sales,
        "title": "Shop Page",
    }

    return render(request, 'useradmin/shop_page.html', context)


def reviews(request):
    reviews = ProductReview.objects.all()
    context = {'reviews': reviews, 'title': 'Reviews'}
    return render(request, 'useradmin/reviews.html', context)


def settings(request):
    profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        image = request.FILES.get('image')
        full_name = request.POST.get('full_name')
        phone = request.POST.get('phone')
        bio = request.POST.get('bio')
        address = request.POST.get('address')
        country = request.POST.get('country')

        if image != None:
            profile.image = image

        profile.full_name = full_name
        profile.phone = phone
        profile.bio = bio
        profile.address = address
        profile.country = country

        profile.save()
        messages.success(request, 'Profile updated successfully')
        return redirect('useradmin:settings')

    context = {
        'profile': profile,
        'title': 'Settings',
    }

    return render(request, 'useradmin/settings.html', context)




