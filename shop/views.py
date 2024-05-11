from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import *
from .models import *


# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'title': 'Barcha productlar',
        'categories': Category.objects.filter(parent=None),
        'page_name': 'Shop'
    }


class AllProductList(ProductList):
    template_name = 'shop/all_products.html'


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'
    extra_context = {
        'title': f"{Product.objects.name} maxsuloti haqida",
        'page_name': 'Shop Detail',
        'categories': Category.objects.filter(parent=None)
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        if self.request.user.is_authenticated:
            rating = Rating.objects.filter(product=product, user=self.request.user).first()
            context['user_rating'] = rating.rating if rating else 0
        return context


def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(id=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return redirect('detail', slug=product.slug)


def user_login(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f'{user.username.title()} saytga xush kelibsiz!')
            return redirect('index')

        if form.errors:
            for error in form.error_messages.values():
                messages.error(request, f"{error}")

    form = LoginForm()
    context = {
        'form': form,
        'title': 'Login page'
    }
    return render(request, 'shop/login.html', context=context)


def user_logout(request):
    logout(request)
    messages.warning(request, "Siz saytdan chiqdingiz!")
    return redirect('login')


def user_register(request):
    form = RegisterForm(data=request.POST)
    if form.is_valid():
        user = form.save()
        messages.success(request, f"{user.username.title()} username va parolingizni kiritib saytga kiring!")
        return redirect('login')

    form = RegisterForm()
    context = {
        'form': form,
        'title': 'Register'
    }
    return render(request, 'shop/register.html', context=context)













# def rating_product(request: HttpRequest) -> HttpResponse:
#     products = Product.objects.all()
#     for product in products:
#         rating = Rating.objects.filter(product=product, user=request.user).first()
#         product.user_rating = rating.rating if rating else 0
#     return render(request, "shop/detail.html", {"products": products})


# def detail(request, slug):
#     product = Product.objects.get(slug=slug)
#     context = {
#         'product': product,
#         'page_name': 'Shop Detail',
#     }
#     return render(request, 'shop/detail.html', context=context)


# def index(request):
#     products = Product.objects.all()
#     categories = Category.objects.all()
#     context = {
#         'products': products,
#         'categories': categories,
#     }
#     return render(request, 'shop/index.html', context=context)


# def test(request):
#     context = {
#         'products': Product.objects.all(),
#         'categories': Category.objects.filter(parent=None)
#     }
#     return render(request, 'shop/all_products.html', context=context)


# def index(request):
#     context = {
#         'categories': Category.objects.all(),
#         'products': Product.objects.all()[:8]
#     }
#     return render(request, 'shop/index.html', context=context)
