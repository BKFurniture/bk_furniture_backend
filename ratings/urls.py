from django.urls import (
    path,
    include
)


from ratings.views import (
    RatingListByProduct,
    RatingDetailViewSet,
)

app_name = 'ratings'

# /products/
rating_detail = RatingDetailViewSet.as_view({
    'get': 'retrieve',
    'patch': 'update',
    'delete': 'destroy'
})

rating_list = RatingDetailViewSet.as_view({
    # 'get': 'list',
    'post': 'create',
})

urlpatterns = [
    path('products/<str:product_slug>/',
         RatingListByProduct.as_view(),
         name='ratings-by-product'),
    path('', rating_list, name='ratings-list'),
    path('<int:pk>', rating_detail, name='ratings-detail'),
]
