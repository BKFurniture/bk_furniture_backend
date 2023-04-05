from rest_framework.generics import RetrieveAPIView, ListAPIView
from rest_framework import generics, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product, Category, CustomDesign

from products import serializers
from .serializers import CustomDesignSerializer, CategorySerializer


class ProductDetail(RetrieveAPIView):
    lookup_field = "slug"
    serializer_class = serializers.ProductDetailSerializer  # same response as using ProductListSerializer
    queryset = Product.objects.all()


class ProductListByCategory(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "avg_rating"]
    ordering = ["price"]

    def get_queryset(self):
        category_slug = self.kwargs['slug']
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
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "avg_rating"]
    ordering = ["price"]

    def get_queryset(self):
        price_range = self.request.query_params.get("price")
        if not price_range:
            return Product.objects.all()
        else:
            lower_bound = price_range.split("-")[0]
            upper_bound = price_range.split("-")[1]
            return Product.objects.filter(price__gte=lower_bound, price__lte=upper_bound)


class CustomDesignStore(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomDesignSerializer
    queryset = CustomDesign.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
