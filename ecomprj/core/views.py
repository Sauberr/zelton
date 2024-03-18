from django.db.models import Avg
from django.shortcuts import render, get_object_or_404
from core.models import Product, Category, Vendor, ProductReview
from taggit.models import Tag


def index(request):
    products = Product.objects.filter(product_status='published', featured=True).order_by('-id')

    context = {'products': products}
    return render(request, 'core/index.html', context)


def product_list_view(request):
    products = Product.objects.filter(product_status='published')
    context = {'products': products}
    return render(request, 'core/product-list.html', context)


def product_detail_view(request, pid):
    product = Product.objects.get(pid=pid)
    # product = get_object_or_404(Product, pid=pid)
    p_image = product.p_images.all()
    products = Product.objects.filter(category=product.category).exclude(pid=pid)
    reviews = ProductReview.objects.filter(product=product).order_by('-date')
    average_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    context = {'p': product, 'p_image': p_image, 'products': products, 'reviews': reviews, 'average_rating': average_rating}
    return render(request, 'core/product-detail.html', context)


def category_list_view(request):
    # categories = Category.objects.all().annotate(product_count=Count('category'))
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'core/category-list.html', context)


def category_product_list_view(request, cid):
    category = Category.objects.get(cid=cid)
    products = Product.objects.filter(product_status='published', category=category)
    context = {'category': category, 'products': products}
    return render(request, 'core/category-product-list.html', context)


def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {'vendors': vendors}
    return render(request, 'core/vendor-list.html', context)


def vendor_detail_view(request, vid):
    vendor = Vendor.objects.get(vid=vid)
    products = Product.objects.filter(vendor=vendor, product_status='published')
    context = {'vendor': vendor, 'products': products}
    return render(request, 'core/vendor-detail.html', context)


def tag_list(request, tag_slug=None):
    products = Product.objects.filter(product_status='published').order_by('-id')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])

    context = {'products': products, 'tag': tag}
    return render(request, 'core/tag.html', context)


