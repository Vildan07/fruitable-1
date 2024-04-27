from django.shortcuts import render, redirect

from .models import Category, Product


# Create your views here.

def index(request):
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/index.html', context=context)
