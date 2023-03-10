from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APIClient

from products.models import Product

from products.serializers import (
    ProductDetailSerializer
)


def detail_url(product_id):
    return reverse('products:product-detail', args=[product_id])


def create_product( **params):
    """
    Create and return sample product
    """
    defaults = {
        'name': 'Sample Product',
        'price': Decimal('25.5'),
        'description': 'Sample Description',
        'origin': 'Sample Company',
        'colors': ['red', 'blue', 'green'],
        'sizes': ['1', '2', '3'],
        'is_custom_design': False
    }
    defaults.update(params)

    product = Product.objects.create(**defaults)
    return product

class PublicProductAPITest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def test_get_product_detail(self):
        product = create_product()

        url = detail_url(product.id)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)
