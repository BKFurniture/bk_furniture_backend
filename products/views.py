from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import generics, filters

from products.models import Product, Category
from products import serializers


class ProductDetail(RetrieveAPIView):
    lookup_field = "slug"
    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()


class ProductListByCategory(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all()

    def get_queryset(self):
        category_slug = self.request.query_params.get('category_slug')
        try:
            category = Category.objects.get(slug=category_slug)
        except Category.DoesNotExist:
            return Product.objects.none()
        queryset = self.queryset
        category_id = category.id
        queryset = queryset.filter(category_id__exact=category_id)
        return queryset.all().order_by('-id').distinct()


class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", ]
    ordering = ["price"]
