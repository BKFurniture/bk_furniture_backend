from rest_framework import (
    viewsets
)

from django.contrib.auth.models import User

from rest_framework.authentication import TokenAuthentication
from rest_framework import permissions
from rest_framework import generics, filters

from . import serializers
from .models import Rating
from products.models import Product
from ratings.permissions import IsOwnerOrReadOnly

# rating list (user): rating/user/user_id

# rating (order_item): rating/rating_id _ CRUD


class RatingListByProduct(generics.ListAPIView):
    serializer_class = serializers.RatingSerializer
    queryset = Rating.objects.all()
    filter_backends = [filters.OrderingFilter]
    ordering_fields = ["stars", "created_at"]
    ordering = ["-created_at"]

    def get_queryset(self):
        queryset = self.queryset
        product_slug = self.kwargs['product_slug']
        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            return Rating.objects.none()
        product_id = product.id
        queryset = queryset.filter(product_id__exact=product_id)
        return queryset.all().order_by('-id').distinct()


class RatingDetailViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.RatingSerializer
    queryset = Rating.objects.all()
    # authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]
    
    def get_queryset(self):
        queryset = self.queryset
        # rating_id = self.kwargs['rating_id']
        # queryset = queryset.filter(id__exact=rating_id)
        return queryset.all().order_by('-id').distinct()

    def perform_create(self, serializer):
        product_slug = self.request.data['product_slug']
        try:
            user = self.request.user
        except User.DoesNotExist:
            raise KeyError('User does not exist')

        try:
            product = Product.objects.get(slug=product_slug)
        except Product.DoesNotExist:
            raise KeyError('Product does not exist')

        serializer.save(user=user, product=product)

    # def delete(self):
    #     return super().retrieve(request, *args, **kwargs)
