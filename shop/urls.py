from django.urls import path
from .views import *

urlpatterns = [
    path('', ProductList.as_view(), name='index'),
    path('products/', AllProductList.as_view(), name='all_products'),
    path('product/<slug:slug>/', ProductDetail.as_view(), name='detail'),
    path('rate/<int:product_id>/<int:rating>/', rate),

    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),
    path('register/', user_register, name='register'),

]