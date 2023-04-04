from django.urls import path

from . import views

# /orders/
urlpatterns = [
    path("checkout/", views.OrderCreateView.as_view(), name="checkout"),
    path("<int:pk>/", views.OrderDetailsView.as_view(), name="order_detail"),
    path("", views.OrderListView.as_view(), name="order_list"),
    path("<int:pk>/cancel/", views.OrderCancelView.as_view(), name="order_cancel"),
]
