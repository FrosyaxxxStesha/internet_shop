from django.shortcuts import render
from catalog.models import Product
from catalog.forms import ProductForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def main(request):
    url_name = 'main'
    products_all = Product.objects.all()
    paginator = Paginator(products_all, per_page=6)
    page_number = request.GET.get('page', 1)
    try:
        products = paginator.page(page_number)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    return render(request, 'catalog/main.html', {'url_name': url_name, 'products': products})


def contact_info(request):
    url_name = 'contact_info'
    return render(request, 'catalog/contact_info.html', {'url_name': url_name})


def contact_form(request):
    url_name = 'contact_form'
    sent = False
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        print(name, email)
        sent = True

    return render(request, 'catalog/contact_form.html', {'url_name': url_name, 'sent': sent})


def product_info(request, product_id):
    product = Product.objects.get(id=product_id)
    context = {
        'name': product.name,
        'description': product.description,
        'photo': product.preview_image,
        'category': product.category.name,
        'price': product.price,
        'created_at': product.created_at,
        'updated_at': product.updated_at
    }
    context = {
        'product': product
    }
    return render(request, 'catalog/product_info.html', context)


def product_form(request):
    product = None
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save()
    else:
        form = ProductForm()
    context = {
        'form': form,
        'product': product,
        'url_name': product_form
    }
    return render(request, 'catalog/product_adding_info.html', context)
