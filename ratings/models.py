from django.db import models
from django.contrib.auth.models import User


class Rating(models.Model):

    class Stars(models.IntegerChoices):
        ONE = 1, '1'
        TWO = 2, '2'
        THREE = 3, '3'
        FOUR = 4, '4'
        FIVE = 5, '5'

    stars = models.IntegerField(
        choices=Stars.choices,
        default=Stars.FIVE,
        )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    order_item = models.OneToOneField(
        'orders.OrderItem',
        related_name='rating',
        primary_key=True,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='ratings',
        on_delete=models.CASCADE,
        null=True
    )
    product = models.ForeignKey(
        'products.Product',
        related_name='ratings',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.order_item}'

    def create(self, **validated_data):
        return Rating.objects.create(**validated_data)


class RatingImage(models.Model):
    rating = models.ForeignKey(
        Rating,
        related_name='images',
        on_delete=models.CASCADE
    )
    url = models.ImageField(null=True, upload_to='rating_images')
