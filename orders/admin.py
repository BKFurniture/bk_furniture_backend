from django.contrib import admin

from .models import Order, OrderItem


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("id", "order", "product", "quantity", "sub_total")


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "order_date", "total_price", "payment_method", "status")
    inlines = [OrderItemInline]
