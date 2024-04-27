from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Категория")
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="Фото")

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
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    price = models.FloatField(verbose_name="Цена")
    discount = models.FloatField(blank=True, null=True, verbose_name="Скидка")
    quantity = models.IntegerField(default=0, verbose_name="Количество")
    slug = models.SlugField(blank=True, null=True)

    color = models.CharField(max_length=10, blank=True, null=True, verbose_name="Цвет")
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name="Время создания" )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ['-pk']
