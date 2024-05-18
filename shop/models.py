from django.contrib.auth.models import User
from django.db import models
from django.db.models import Avg


# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Категория")
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="category/", blank=True, null=True, verbose_name="Фото")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subcategories')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['-pk']


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name="Продукт")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Фото")
    description = models.TextField(blank=True, null=True, verbose_name="Описание")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория", related_name='products')
    price = models.FloatField(verbose_name="Цена")
    discount = models.FloatField(blank=True, null=True, verbose_name="Скидка")
    quantity = models.IntegerField(default=0, verbose_name="Количество")
    slug = models.SlugField(blank=True, null=True)
    is_sale = models.IntegerField(default=0)

    color = models.CharField(max_length=10, blank=True, null=True, verbose_name="Цвет")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Время создания")

    @property
    def full_price(self):
        if self.is_sale > 0:
            sale_price = self.price * self.is_sale / 100
            return round(self.price - sale_price, 2)
        else:
            return self.price

    @property
    def avg_rating(self):
        ratings = self.rating_set.all()
        if ratings:
            count = 0
            for rating in ratings:
                count += rating.rating
            return int(count / len(ratings))
        else:
            return 0

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-pk']


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.user} - {self.product.name} - {self.rating}"

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинги продуктов'
        ordering = ['-pk']


class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    name = models.CharField(max_length=150, null=True)
    email = models.EmailField(null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True)
    added = models.DateTimeField(auto_now_add=True)


"""Models for Cart"""


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    first_name = models.CharField(max_length=150, null=True, blank=True)
    last_name = models.CharField(max_length=150, null=True, blank=True)


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        total_price = sum([product.get_total_price for product in order_products])
        return total_price

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        total_quantity = len(order_products)
        return total_quantity


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    @property
    def get_total_price(self):
        total_price = self.quantity * self.product.price
        return round(total_price, 2)


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=255)
    district = models.ForeignKey('Region', on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey('City', on_delete=models.SET_NULL, null=True)
    zip_code = models.IntegerField()
    mobile = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)


class Region(models.Model):
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


class City(models.Model):
    region = models.ForeignKey(Region, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=150)

    def __str__(self):
        return self.name


