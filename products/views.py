from rest_framework.generics import RetrieveAPIView, ListAPIView

from django.db.models import Avg, Count, Q, Value, FloatField
from django.db.models.functions import Coalesce

from rest_framework import generics, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product, Category, CustomDesign

from products import serializers
from products.models import Product, Category
from .serializers import CustomDesignSerializer, CategorySerializer



class ProductDetail(RetrieveAPIView):
    lookup_field = "slug"
    serializer_class = serializers.ProductDetailSerializer  # same response as using ProductListSerializer
    queryset = Product.objects.all()


class ProductListByCategory(ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.annotate(
        count_rating=Count('ratings'),
    )
    queryset = queryset.annotate(
        avg_rating=Coalesce(
            Avg('ratings__stars', output_field=FloatField()),
            Value(0, output_field=FloatField()),
        )
    )
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
        # print(queryset.values('count_rating', 'avg_rating'))
        return queryset.all().order_by('-count_rating', '-id').distinct()


class ProductList(generics.ListAPIView):
    serializer_class = serializers.ProductListSerializer
    queryset = Product.objects.annotate(
        count_rating=Count('ratings'),
    )
    queryset = queryset.annotate(
        avg_rating=Coalesce(
            Avg('ratings__stars', output_field=FloatField()),
            Value(0, output_field=FloatField()),
        )
    )
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["price", "avg_rating"]
    ordering = ["price"]

    def get_queryset(self):
        queryset = self.queryset
        price_range = self.request.query_params.get("price")
        if not price_range:
            return queryset.all()
        else:
            lower_bound = price_range.split("-")[0]
            upper_bound = price_range.split("-")[1]
            return queryset.filter(price__gte=lower_bound, price__lte=upper_bound)



class CustomDesignStore(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomDesignSerializer
    queryset = CustomDesign.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
