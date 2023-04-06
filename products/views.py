from django.shortcuts import render, redirect
from products.models import Product, Review
from products.forms import ProductCreateForm, ReviewCreateForm
from products.constants import PAGINATION_LIMIT


def main_view(request):
    if request.method == 'GET':
        return render(request, 'layouts/index.html')


def products_view(request):
    if request.method == 'GET':
        products = Product.objects.all()
        search = request.GET.get('search')
        page = int(request.GET.get('page', 1))
        if search:
            products = products.filter(name__icontains=search) | products.filter(description__icontains=search)
        max_page = products.__len__() / PAGINATION_LIMIT
        max_page = round(max_page) + 1 if round(max_page) < max_page else round(max_page)
        products = products[PAGINATION_LIMIT * (page - 1): PAGINATION_LIMIT * page]
        context = {
            'products': products,
            'user': request.user,
            'pages': range(1, max_page + 1)
        }
        return render(request, 'products/products.html', context=context)


def product_detail_view(request, id):
    if request.method == 'GET':
        product = Product.objects.get(id=id)
        context = {
            'product': product,
            'reviews': product.review_set.all(),
            'form': ReviewCreateForm,
            'user': request.user
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
