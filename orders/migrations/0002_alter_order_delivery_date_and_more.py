# Generated by Django 4.1.7 on 2023-04-03 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="delivery_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="expected_delivery_date",
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="order_date",
            field=models.DateField(auto_now_add=True),
        ),
    ]
