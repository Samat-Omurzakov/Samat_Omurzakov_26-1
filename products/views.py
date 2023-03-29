from django.shortcuts import render, redirect
from products.models import Product, Review
from products.forms import ProductCreateForm, ReviewCreateForm


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        context = {
            'products': products
        }
        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'reviews': product.review_set.all(),
            'form': ReviewCreateForm
        }
        return render(request, 'products/detail.html', context=context)
    if request.method == "POST":
        product = Product.objects.get(id=id)
        form = ReviewCreateForm(data=request.POST)

    if form.is_valid():
        Review.objects.create(
            text=form.cleaned_data.get('text'),
            product_id=id
        )

    context = {
        'product': product,
        'reviews': product.review_set.all(),
        'form': form
    }
    return render(request, 'products/detail.html', context=context)


def product_create_view(request):
    if request.method == 'GET':
        context = {
            'form': ProductCreateForm
        }
        return render(request, 'products/create.html', context=context)

    if request.method == 'POST':
        form = ProductCreateForm(request.POST, request.FILES)

        if form.is_valid():
            Product.objects.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                image=form.cleaned_data.get('image')
            )
            return redirect('/products/')
        return render(request, 'products/create.html', context={
            'form': form
        })
