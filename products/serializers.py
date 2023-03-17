from rest_framework import serializers

from products.models import Product, ProductImage, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'slug',
        ]


class ProductDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category', 'price', 'description',
                  'origin', 'colors', 'sizes', 'is_custom_design']
        read_only_fields = ['id']


class ProductImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductImage
        fields = [
            "url",
        ]


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
