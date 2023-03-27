from decimal import Decimal

from django.test import TestCase
from django.urls import reverse

# from rest_framework import status
from rest_framework.test import APIClient

from products.models import Product, Category
from products.serializers import (
    ProductDetailSerializer,
    ProductListSerializer
)

PRODUCT_BY_CATEGORY_URL = reverse('products:product-by-category')


def detail_url(product_slug):
    return reverse('products:product-detail', args=[product_slug])


def create_product(**params):
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

        url = detail_url(product.slug)
        res = self.client.get(url)

        serializer = ProductDetailSerializer(product)
        self.assertEqual(res.data, serializer.data)

    def test_filter_product_by_category(self):
        category1 = Category.objects.create(
            title='Sample Category'
        )
        category2 = Category.objects.create(
            title='Sample Category 2'
        )
        p1 = create_product(
            name='Sample Product',
            price=109.99,
            description='Sample Description',
            origin='Sample Company',
            colors=['red', 'blue', 'green'],
            sizes=['1', '2', '3'],
            is_custom_design=False,
            category=category1
        )
        p2 = create_product(
            name='Sample Product 2',
            price=99.99,
            description='Sample Description',
            origin='Sample Company',
            colors=['wood', 'black'],
            sizes=['1'],
            is_custom_design=False,
            category=category2
        )
        params = {'category_slug': f'{category1.slug}'}
        res = self.client.get(PRODUCT_BY_CATEGORY_URL, params)

        s1 = ProductListSerializer(p1)
        s2 = ProductListSerializer(p2)
        self.assertIn(s1.data, res.data)
        self.assertNotIn(s2.data, res.data)
