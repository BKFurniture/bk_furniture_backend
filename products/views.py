from rest_framework.generics import RetrieveAPIView
from rest_framework import generics, filters

from products.models import Product
from products import serializers


class ProductDetail(RetrieveAPIView):
    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()


class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price",]
    ordering = ["price"]
