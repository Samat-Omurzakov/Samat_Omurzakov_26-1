from django.shortcuts import render, redirect
from products.models import Product, Review
from products.forms import ProductCreateForm, ReviewCreateForm
from products.constants import PAGINATION_LIMIT
from django.views.generic import ListView, CreateView, DetailView


class MainPageCBV(ListView):
    model = Product
    template_name = 'layouts/index.html'


class ProductCBV(ListView):
    model = Product
    template_name = 'products/products.html'

    def get(self, request, **kwargs):
        products = self.get_queryset()
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
        return render(request, self.template_name, context=context)


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


class ProductDetailCBV(DetailView, CreateView):
    model = Product
    template_name = 'products/detail.html'
    form_class = ReviewCreateForm
    pk_url_kwarg = 'id'

    # def get_context_data(self, *, object_list=None, **kwargs):
    #     return {
    #         'product': self.get_object(),
    #         'reviews': Review.objects.filter(product=self.get_object()),
    #         'form': self.form_class,
    #         'user': request.user
    #     }

    def get(self, request, **kwargs):
        context = {
            'product': self.get_object(),
            'id': self.get_object().id,
            'reviews': Review.objects.filter(product=self.get_object()),
            'form': self.form_class,
            'user': request.user
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        # product = Product.objects.get(id=id)
        form = self.form_class(data=request.POST)

        if form.is_valid():
            Review.objects.create(
                text=form.cleaned_data.get('text'),
                product_id=id
            )

        context = {
            'product': self.get_object(),
            'id': self.get_object().id,
            'reviews': Review.objects.filter(product=self.get_object()),
            'form': form
        }
        return render(request, self.template_name, context=context)


class ProductCreateCBV(ListView, CreateView):
    model = Product
    template_name = 'products/create.html'
    form_class = ProductCreateForm

    def get_context_data(self, *, object_list=None, **kwargs):
        return {
            'form': kwargs['form'] if kwargs.get('form') else self.form_class
        }

    def get(self, requset, **kwargs):
        return render(requset, self.template_name, context=self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if form.is_valid():
            self.model.objects.create(
                name=form.cleaned_data.get('name'),
                description=form.cleaned_data.get('description'),
                price=form.cleaned_data.get('price'),
                image=form.cleaned_data.get('image')
            )
            return redirect('/products/')
        return render(request, self.template_name, context=self.get_context_data(form=form))
