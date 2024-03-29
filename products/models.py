from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from django_jsonform.models.fields import ArrayField


class Category(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return f'/{self.slug}/'


class Product(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, null=True)
    category = models.ForeignKey(
        Category,
        related_name='products',
        null=True,
        blank=True,
        on_delete=models.SET_NULL
    )
    price = models.DecimalField(max_digits=9, decimal_places=2, default=99.99)
    description = models.TextField(null=True, blank=True)
    origin = models.CharField(max_length=255, null=True, blank=True)
    colors = ArrayField(models.CharField(max_length=20), 6)
    sizes = ArrayField(models.TextField(), 4)
    is_custom_design = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'


class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name="images", on_delete=models.CASCADE)
    url = models.ImageField(upload_to="product_images/")

    def __str__(self):
        return f'{self.product.name} - {self.id}'


class CustomDesign(models.Model):
    user = models.ForeignKey(User, related_name="custom_designs", on_delete=models.CASCADE)
    description = models.TextField(max_length=1023, null=True, blank=True)

    def __str__(self):
        return f'{self.id} - {self.user.username}'


class CustomDesignImage(models.Model):
    custom_design = models.ForeignKey(
        CustomDesign,
        related_name="custom_design_images",
        on_delete=models.CASCADE
    )
    url = models.ImageField(upload_to="custom_design_images/")
