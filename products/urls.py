from django.urls import (
    path,
    # include
)

from products.views import ProductDetail, ProductListByCategory
from . import views

app_name = 'products'

# /products/
urlpatterns = [
    path('detail/<str:slug>', ProductDetail.as_view(), name='product-detail'),
    path('products/',
         ProductListByCategory.as_view(),
         name='product-by-category'),
    path("", views.ProductList.as_view(), name="product-list"),
]
