# Generated by Django 4.1.7 on 2023-04-04 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_alter_order_discount_alter_order_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="recipient_name",
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
    ]