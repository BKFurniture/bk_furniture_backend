from django.urls import (
    path,
    # include
)


from products.views import ProductDetail, ProductListByCategory

from . import views

app_name = 'products'

# /products/
urlpatterns = [
    path("create-product-image/", views.ProductImageCreate.as_view()),
    path("custom-design/", views.CustomDesignStore.as_view(), name="create-custom-design"),
    path("category-list/", views.CategoryList.as_view(), name="category-list"),
    path('detail/<str:slug>', ProductDetail.as_view(), name='product-detail'),
    path('<str:slug>/',
         ProductListByCategory.as_view(),
         name='product-by-category'),
    path("", views.ProductList.as_view(), name="product-list"),
]
