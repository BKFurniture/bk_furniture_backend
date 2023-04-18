# Generated by Django 4.1.7 on 2023-04-04 17:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0004_order_recipient_name'),
        ('ratings', '0002_remove_rating_is_updated'),
    ]

    operations = [
        migrations.AddField(
            model_name='rating',
            name='order_item',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='orders.orderitem'),
        ),
    ]
