from rest_framework import serializers

from products.models import Product


class ProductDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'name', 'slug', 'category',
           'price', 'description', 'origin',
            'colors', 'sizes', 'is_custom_design']
        read_only_fields = ['id']


class ProductListSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = "__all__"
