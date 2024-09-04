from django.contrib import admin
from django.utils.html import format_html

from .models import Profile, Question, WishList
from .models import Category, Product, ProductImage, Characteristic, ProductCharacteristicValue, Comment

admin.site.register(Profile)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ['parent']


admin.site.register(Category, CategoryAdmin)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1  # Number of empty forms to display in the admin


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created', 'updated']
    list_filter = ['available', 'created', 'updated']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline]
    search_fields = ['name', 'slug', 'description', 'category__name']


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('product', 'author', 'published_date', 'content', 'answer')
    search_fields = ('content', 'answer')


@admin.register(WishList)
class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'display_products')

    def display_products(self, obj):
        return format_html("<br>".join([product.name for product in obj.products.all()]))

    display_products.short_description = 'Products'


@admin.register(Characteristic)
class Characteristic(admin.ModelAdmin):
    search_fields = ('name',)


@admin.register(ProductCharacteristicValue)
class ProductCharacteristicValue(admin.ModelAdmin):
    list_filter = ['product', 'characteristic']
    search_fields = ('characteristic__name',)


admin.site.register(Product, ProductAdmin)
admin.site.register(Comment)





