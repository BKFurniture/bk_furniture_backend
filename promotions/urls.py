from django.urls import path

from . import views

# /promotions/
urlpatterns = [
    path("coupon-check/<str:code>/", views.CouponCheckView.as_view(), name="coupon-check"),
]
