from django.http import Http404

from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .serializers import OrderSerializer, OrderCreateSerializer
from .models import Order


class IsOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user


class OrderCreateView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderCreateSerializer
    queryset = Order.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderDetailsView(generics.RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated, IsOwner]
    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderListView(generics.ListAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderSerializer

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


class OrderCancelView(APIView):

    def put(self, request, pk, format=None):
        try:
            order_instance = Order.objects.get(id=pk)
        except Order.DoesNotExist:
            raise Http404
        order_instance.status = "canceled"
        order_instance.save()
        return Response(status=status.HTTP_200_OK)
