from rest_framework.generics import RetrieveAPIView, ListAPIView

from django.db.models import Avg, Count, Q, Value, FloatField
from django.db.models.functions import Coalesce

from rest_framework import generics, filters, status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from products.models import Product, Category, CustomDesign, ProductImage

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
        price_range = self.request.query_params.get("price")
        if not price_range:
            return queryset.filter(
                category_id=category_id
                ).order_by('-count_rating', '-id')
        else:
            lower_bound = price_range.split("-")[0]
            upper_bound = price_range.split("-")[1]
            return queryset.filter(
                price__gte=lower_bound,
                price__lte=upper_bound,
                category_id=category_id).order_by('-count_rating', '-id')


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
    ordering_fields = [
        "price",
        "avg_rating"
    ]
    ordering = ["price"]

    def get_queryset(self):
        queryset = self.queryset
        price_range = self.request.query_params.get("price")
        if not price_range:
            return queryset.all()
        else:
            lower_bound = price_range.split("-")[0]
            upper_bound = price_range.split("-")[1]
            return queryset.filter(
                price__gte=lower_bound,
                price__lte=upper_bound
                )


class CustomDesignStore(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CustomDesignSerializer
    queryset = CustomDesign.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CategoryList(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class ProductImageCreate(generics.CreateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = serializers.ProductImageCreateSerializer
    queryset = ProductImage.objects.all()


class ProductListCreate(APIView):
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, format=None):
        ser = serializers.ProductListCreateSerializer(data=request.data, many=True)
        if ser.is_valid():
            ser.save()
            return Response(ser.data, status=status.HTTP_201_CREATED)
        return Response(ser.errors, status=status.HTTP_400_BAD_REQUEST)


# More consideration
# class ProductImageCreate(APIView):
#     permission_classes = [permissions.AllowAny]

#     def post(self, request, format=None):
#         print(request.data)
#         product_ids = request.data.get('product_ids').split(',')
#         print(request.data.get("url1"))
#         for id in product_ids:
#             imgs = request.data.get(f'url{int(id)}')
#             data = {
#                 "product": id
#             }
#             data["urls"] = imgs
#             print(data)
#             ser = serializers.ProductImageCreateSerializer(data=data)
#             if ser.is_valid():
#                 ser.save()
#         return Response("OK", status=status.HTTP_201_CREATED)
