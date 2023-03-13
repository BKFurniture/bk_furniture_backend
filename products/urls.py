from django.urls import (
    path,
    include
)

# from rest_framework.routers import DefaultRouter

from products.views import ProductDetail

# router = DefaultRouter()
# router.register('', views.RecipeViewSet)

app_name = 'products'

# /products/
urlpatterns = [
    path('detail/<int:pk>', ProductDetail.as_view(), name='product-detail'),
]
