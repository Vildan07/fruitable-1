from django.contrib import messages
from django.contrib.auth import login, logout
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import stripe
from django.conf import settings

from .forms import CheckoutForm, LoginForm, RegisterForm, ReviewForm
from .models import *
from .utils import CartAuthenticatedUser

# Create your views here.


class ProductList(ListView):
    model = Product
    template_name = 'shop/index.html'
    context_object_name = 'products'
    extra_context = {
        'title': 'Barcha productlar',
        'categories': Category.objects.filter(parent=None),
        'page_name': 'Shop',
        # 'subcategories': Category.objects.filter(parent=products)
    }

    def get_queryset(self):
        return Product.objects.filter(is_sale=0)


class AllProductList(ProductList):
    template_name = 'shop/all_products.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        products = Product.objects.exclude(is_sale=0).order_by('-is_sale')[:3]
        context['sale_products'] = products
        return context


def by_is_sale(request):
    context = {
        'products': Product.objects.exclude(is_sale=0),
        'page_name': "All Sale Products"
    }
    return render(request, 'shop/all_products.html', context=context)


class ProductDetail(DetailView):
    model = Product
    template_name = 'shop/detail.html'
    context_object_name = 'product'
    extra_context = {
        'title': f"{Product.objects.name} maxsuloti haqida",
        'page_name': 'Shop Detail',
        'categories': Category.objects.filter(parent=None),
        'reviews': Review.objects.filter,
        'products': Product.objects.all(),
        'orderproduct': OrderProduct.objects.all()

    }

    def get_context_data(self, **kwargs):
        self.products = Product.objects.exclude(is_sale=0).order_by('-is_sale')[:3]
        context = super().get_context_data(**kwargs)
        product = Product.objects.get(slug=self.kwargs['slug'])
        context['sale_products'] = self.products
        if self.request.user.is_authenticated:
            rating = Rating.objects.filter(product=product, user=self.request.user).first()
            context['user_rating'] = rating.rating if rating else 0
            context['reviews'] = Review.objects.filter(author=self.request.user, product=product).order_by('-added')
        return context

    # def to_cart_detail(self, request: HttpRequest, product_id, action) -> HttpResponse:
    #     if request.user.is_authenticated:
    #         CartAuthenticatedUser(request, product_id, action)
    #         page = self.request.META.get('HTTP_REFERER')
    #         return redirect(page)
    #     else:
    #         return redirect('login')



def rate(request: HttpRequest, product_id: int, rating: int) -> HttpResponse:
    product = Product.objects.get(id=product_id)
    Rating.objects.filter(product=product, user=request.user).delete()
    product.rating_set.create(user=request.user, rating=rating)
    return redirect('detail', slug=product.slug)


def cart(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        cart_info = CartAuthenticatedUser(request).get_cart_info()
        context = {
            'order_products': cart_info['order_products'],
            'cart_total_price': cart_info['cart_total_price'],
            'cart_total_quantity': cart_info['cart_total_quantity'],
            'page_name': 'Cart',
        }
        return render(request, 'shop/cart.html', context=context)
    else:
        return redirect('login')


def to_cart(request: HttpRequest, product_id, action) -> HttpResponse:
    if request.user.is_authenticated:
        CartAuthenticatedUser(request, product_id, action)
        page = request.META.get('HTTP_REFERER')
        return redirect(page)
    else:
        return redirect('login')

def create_checkout_session(request: HttpRequest) -> HttpResponse:
    stripe.api_key = settings.STRIPE_SECRET_KEY
    user_cart = CartAuthenticatedUser(request)
    cart_info = user_cart.get_cart_info()
    total_price = cart_info['cart_total_price']
    total_quantity = cart_info['cart_total_quantity']
    session = stripe.checkout.Session.create(
        line_items=[{
            'price_data': {
                'currency': 'usd',
                'product_data': {
                    'name': 'Online Shop mahsulotlari'
                },
                'unit_amount': int(total_price * 100),
            },
            'quantity': total_quantity
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('success_payment')),
        cancel_url=request.build_absolute_uri(reverse('error_payment')),
    )
    return redirect(session.url, 303)


def success_payment(request: HttpRequest) -> HttpResponse:
    return render(request, 'shop/success.html')


def error_payment(request: HttpRequest) -> HttpResponse:
    return render(request, 'shop/error.html')


def checkout(request: HttpRequest) -> HttpResponse:
    form = CheckoutForm(request.POST)
    if form.is_valid():
        form.save()
    else:
        form = CheckoutForm()
    context = {
        'form': form,
        'page_name': 'Checkout',
    }
    return render(request, 'shop/checkout.html', context=context)








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


def save_review(request: HttpRequest, product_slug):
    if request.user.is_authenticated:
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            product = Product.objects.get(slug=product_slug)
            review = form.save(commit=False)
            review.product = product
            review.author = request.user
            review.save()
        return redirect('detail', slug=product_slug)
    else:
        return redirect('login')














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
