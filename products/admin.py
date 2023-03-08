from django.contrib import admin
from .models import Category, Product, ProductImage


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "product")


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "category", "price")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline]


class ProductInline(admin.TabularInline):
    model = Product
    extra = 0


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "title",)
    inlines = [ProductInline]
    prepopulated_fields = {"slug": ("title",)}
