# Generated by Django 4.1.7 on 2023-04-16 05:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Coupon",
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
                ("code", models.CharField(max_length=63)),
                ("discount", models.PositiveSmallIntegerField()),
                ("usage_limit", models.PositiveSmallIntegerField()),
                ("is_active", models.BooleanField(default=True)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "selected_users",
                    models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL),
                ),
                (
                    "user_blocklist",
                    models.ManyToManyField(
                        blank=True,
                        related_name="used_coupons",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]