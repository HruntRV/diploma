from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='user_avatar')
    phone = models.CharField(max_length=15, blank=True, unique=True)
    country = models.CharField(max_length=25, blank=True)
    city = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=6, blank=True)
    main_delivery_address = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True, unique=True)
    image = models.ImageField(upload_to='category_image', blank=True)
    parent = models.ForeignKey('self', related_name='subcategories', on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        ordering = ('name',)
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('market:product_list_by_category', args=[self.slug])

    def get_full_path(self):
        if self.parent:
            return f"{self.parent.get_full_path()} > {self.name}"
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    # image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('name',)
        indexes = [
            models.Index(fields=['id', 'slug']),
        ]
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('market:product_detail',
                       args=[self.id, self.slug])


def product_image_upload_to(instance, filename):
    category_slug = instance.product.category.name
    product_id = instance.product.id
    return f'products/{category_slug}/{product_id}/{filename}'


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=product_image_upload_to)
    alt_text = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Image for {self.product.name}"


class Comment(models.Model):
    product = models.ForeignKey('Product', related_name='comment', on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"Comment for {self.product.name}"

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class Question(models.Model):
    product = models.ForeignKey('Product', related_name='question', on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    content = models.TextField(verbose_name='Контент')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, default=1)
    answer = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Question for {self.product.name}"

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'


class Characteristic(models.Model):
    category = models.ForeignKey('Category', related_name='characteristics', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50, blank=True, null=True)  # e.g., "inches", "MP", etc.

    def __str__(self):
        return f"{self.name} ({self.unit})" if self.unit else self.name

    class Meta:

        verbose_name = 'Характеристика'
        verbose_name_plural = 'Характеристики'


class ProductCharacteristicValue(models.Model):
    product = models.ForeignKey('Product', related_name='characteristic_values', on_delete=models.CASCADE)
    characteristic = models.ForeignKey('Characteristic', related_name='values', on_delete=models.CASCADE)
    value = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.characteristic.name}: {self.value} {self.characteristic.unit or ''}"

    class Meta:
        ordering = ['characteristic']
        verbose_name = 'Характеристики товара'
        verbose_name_plural = 'Характеристики товара'


class WishList(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField('Product', related_name='wishlists')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


