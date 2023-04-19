# Generated by Django 4.1.7 on 2023-04-03 04:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("products", "0003_rename_image_productimage_url_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("address", models.CharField(blank=True, max_length=255, null=True)),
                ("order_date", models.DateTimeField(auto_now_add=True)),
                ("expected_delivery_date", models.DateTimeField(blank=True, null=True)),
                ("delivery_date", models.DateTimeField(blank=True, null=True)),
                (
                    "mobile",
                    phonenumber_field.modelfields.PhoneNumberField(
                        blank=True, max_length=128, null=True, region=None
                    ),
                ),
                (
                    "discount",
                    models.PositiveSmallIntegerField(
                        blank=True, help_text="discount percents off", null=True
                    ),
                ),
                (
                    "total_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("to_pay", "To Pay"),
                            ("on_delivery", "On Delivery"),
                            ("delivered", "Delivered"),
                            ("canceled", "Canceled"),
                        ],
                        default="to_pay",
                        max_length=15,
                    ),
                ),
                (
                    "payment_method",
                    models.CharField(
                        choices=[("paypal", "Paypal"), ("cash", "Cash")],
                        default="paypal",
                        max_length=15,
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("quantity", models.PositiveIntegerField(blank=True, null=True)),
                (
                    "sub_total",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=6, null=True
                    ),
                ),
                (
                    "order",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order_items",
                        to="orders.order",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]