from django.contrib import admin
from .models import Category, Product, ProductImage, CustomDesign, CustomDesignImage


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


@admin.register(CustomDesignImage)
class CustomDesignImageAdmin(admin.ModelAdmin):
    list_display = ("id", "custom_design", "url")


class CustomDesignImageInline(admin.TabularInline):
    model = CustomDesignImage
    extra = 0


@admin.register(CustomDesign)
class CustomDesignAdmin(admin.ModelAdmin):
    list_display = ("id", "user")
    inlines = [CustomDesignImageInline]
