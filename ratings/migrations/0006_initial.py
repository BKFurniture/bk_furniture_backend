# Generated by Django 4.1.7 on 2023-04-04 17:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('orders', '0004_order_recipient_name'),
        ('products', '0003_rename_image_productimage_url_and_more'),
        ('ratings', '0005_remove_ratingimage_rating_delete_rating_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('stars', models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], default=5)),
                ('comment', models.TextField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('order_item', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='rating', serialize=False, to='orders.orderitem')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='products.product')),
            ],
        ),
        migrations.CreateModel(
            name='RatingImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.ImageField(null=True, upload_to='rating_images')),
                ('rating', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='ratings.rating')),
            ],
        ),
    ]
