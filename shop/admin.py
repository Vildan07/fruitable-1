from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *
# Register your models here.


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'quantity', 'price', 'category', 'get_image')
    list_display_links = ('name',)
    list_editable = ('quantity', 'price', 'category')
    list_filter = ('category',)
    search_fields = ('name', 'description')

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" style="border-radius: 20px;">')
        else:
            return mark_safe(f'<img src="{"https://ami.by/thumbs/getthumb.php?w%5Cu003d200%5Cu0026h%5Cu003d267%5Cu0026src%5Cu003dimages/catalogue/items/sofa_prestizh_02.jpg"}" width="100px" style="border-radius: 20px;">')

    get_image.short_description = 'Фото'
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'parent', 'get_image')
    list_display_links = ('name',)
    list_filter = ('image',)
    search_fields = ('name',)

    def get_image(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" width="100px" style="border-radius: 20px;">')
        else:
            return mark_safe(f'<img src="{"https://ami.by/thumbs/getthumb.php?w%5Cu003d200%5Cu0026h%5Cu003d267%5Cu0026src%5Cu003dimages/catalogue/items/sofa_prestizh_02.jpg"}" width="100px" style="border-radius: 20px;">')

    get_image.short_description = 'Фото'
    prepopulated_fields = {'slug': ('name',)}


class RatingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'product', 'rating')


admin.site.register(Rating, RatingAdmin)