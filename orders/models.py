from django.db import models
from django.contrib.auth.models import User

from phonenumber_field.modelfields import PhoneNumberField

from products.models import Product


class Order(models.Model):
    ORDER_STATUS_CHOICES = [
        ("processing", "Processing"),
        ("on_delivery", "On Delivery"),
        ("delivered", "Delivered"),
        ("canceled", "Canceled"),
    ]
    PAYMENT_METHOD_CHOICES = [
        ("paypal", "Paypal"),
        ("cash", "Cash"),
    ]
    user = models.ForeignKey(User, related_name="orders", on_delete=models.CASCADE, null=True)
    recipient_name = models.CharField(max_length=63, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    order_date = models.DateField(auto_now_add=True, blank=True)
    expected_delivery_date = models.DateField(null=True, blank=True)
    delivery_date = models.DateField(null=True, blank=True)
    mobile = PhoneNumberField(null=True, blank=True)
    discount = models.CharField(
        max_length=63, null=True, blank=True,
        help_text="coupon code"
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=15, choices=ORDER_STATUS_CHOICES, default="processing")
    payment_method = models.CharField(max_length=15, choices=PAYMENT_METHOD_CHOICES, default="paypal")

    def __str__(self):
        if self.user is not None:
            return str(self.id) + "-" + self.user.username
        return str(self.id) + "-"


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    sub_total = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    color = models.CharField(max_length=20, null=True, blank=True)
    size = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.order) + "-" + str(self.id) + "-" + str(self.product.slug)
