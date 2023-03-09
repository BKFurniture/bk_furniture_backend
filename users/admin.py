from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone")
