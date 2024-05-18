from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductList.as_view(), name='all_products'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='detail'),
    path('rate/<int:product_id>/<int:rating>/', rate),
    path('save-review/<slug:product_slug>/', save_review, name='save_review'),
    path('all-sale-products/', by_is_sale, name='by_is_sale'),
    path('cart/', cart, name='cart'),
    path('to-cart/<int:product_id>/<str:action>', to_cart, name='to_cart'),
    path('product/<slug:slug>/to-cart/<int:product_id>/<str:action>', to_cart, name='to_cart'),
    path('checkout/', checkout, name='checkout'),

    path('payment/', create_checkout_session, name='payment'),
    path('success-payment/', success_payment, name='success_payment'),
    path('error-payment/', error_payment, name='error_payment'),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),

]