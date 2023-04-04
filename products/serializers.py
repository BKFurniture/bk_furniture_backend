from rest_framework import serializers

from django.db.models import Avg
from decimal import Decimal

from products.models import Product, ProductImage
from ratings.serializers import RatingSerializer, RatingDisplaySerializer


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "url",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    images = ProductImageSerializer(many=True, read_only=True, required=False)
    ratings = RatingDisplaySerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = ['id',
                  'name',
                  'slug',
                  'category',
                  'price',
                  'description',
                  'origin',
                  'colors',
                  'sizes',
                  'is_custom_design',
                  'category',
                  'images',
                  'ratings'
                  ]
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    images = ProductImageSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "slug",
            "category",
            "price",
            "description",
            "origin",
            "colors",
            "sizes",
            "is_custom_design",
            "images",
            "avg_rating",
            "count_rating",
        ]

    avg_rating = serializers.SerializerMethodField()
    count_rating = serializers.SerializerMethodField()

    def get_avg_rating(self, ob):
        stars_avg = ob.ratings.all().aggregate(Avg('stars'))['stars__avg']
        return stars_avg if stars_avg else Decimal(0.0)

    def get_count_rating(self, ob):
        count_rating = ob.ratings.all().count()
        return count_rating
