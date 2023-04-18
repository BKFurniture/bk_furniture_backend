from django.shortcuts import get_object_or_404

from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Coupon


class CouponCheckView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Coupon.objects.all()

    def get_object(self, code):
        return get_object_or_404(Coupon, code=code)

    def get(self, request, code, format=None):
        coupon_instance = self.get_object(code)
        response = None
        if not coupon_instance.is_valid():
            response = "Invalid Coupon Code"
        if not coupon_instance.is_valid_user(request.user):
            response = "Invalid User"
        response = {
            "discount_percentage": coupon_instance.discount,
            "usage_limit": coupon_instance.usage_limit
        }
        return Response(response, status=status.HTTP_200_OK)
