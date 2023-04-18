# Generated by Django 4.1.7 on 2023-04-16 07:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0004_order_recipient_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="discount",
            field=models.CharField(
                blank=True, help_text="coupon code", max_length=63, null=True
            ),
        ),
    ]
