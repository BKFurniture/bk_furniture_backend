from rest_framework import serializers

from products.models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "url",
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    images = ProductImageSerializer(many=True, read_only=True, required=False)

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
                  'images']
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField(many=False)
    images = ProductImageSerializer(many=True, read_only=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "description",
            "origin",
            "colors",
            "sizes",
            "is_custom_design",
            "images",
        ]
