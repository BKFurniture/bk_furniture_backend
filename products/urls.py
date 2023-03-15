from django.urls import (
    path,
    # include
)

from products.views import ProductDetail
from . import views

app_name = 'products'

# /products/
urlpatterns = [
    path('detail/<int:pk>', ProductDetail.as_view(), name='product-detail'),
    path("", views.ProductList.as_view(), name="product-list"),
]
