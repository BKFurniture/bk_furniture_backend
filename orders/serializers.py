from rest_framework import serializers

from .models import Order, OrderItem
from products.serializers import ProductDetailSerializer, ProductListSerializer
from ratings.serializers import RatingSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductListSerializer(many=False)
    rating = RatingSerializer(many=False, read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "order",
            "quantity",
            "sub_total",
            "rating",
            "color",
            "size"
        ]


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "recipient_name",
            "address",
            "order_date",
            "expected_delivery_date",
            "delivery_date",
            "mobile",
            "discount",
            "total_price",
            "status",
            "payment_method",
            "order_items",
        ]


class OrderItemCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "order",
            "quantity",
            "sub_total",
            "color",
            "size"
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    order_items = OrderItemCreateSerializer(many=True, read_only=False)

    class Meta:
        model = Order
        fields = [
            "id",
            "recipient_name",
            "address",
            "order_date",
            "expected_delivery_date",
            "delivery_date",
            "mobile",
            "discount",
            "total_price",
            "status",
            "payment_method",
            "order_items",
        ]

    def create(self, validated_data):
        order_items = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)
        for item in order_items:
            OrderItem.objects.create(order=order, **item)
        return order
