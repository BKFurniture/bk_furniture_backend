from rest_framework.generics import RetrieveAPIView


from products.models import Product
from products import serializers


class ProductDetail(RetrieveAPIView):
    serializer_class = serializers.ProductDetailSerializer
    queryset = Product.objects.all()
