import tempfile
import shutil
import os

from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.exceptions import ValidationError
from rest_framework.test import APIClient

from .models import Product
from categories.models import Category


class ProductModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='owner', password='pass')
        self.category = Category.objects.create(name='TestCat', slug='testcat')

    def test_price_validation(self):
        img = SimpleUploadedFile('img.jpg', b'content', content_type='image/jpeg')
        p = Product(
            product_name='P', slug='p', description='d', price=0,
            images=img, stock=1, category=self.category, created_by=self.user
        )
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_stock_validation(self):
        img = SimpleUploadedFile('img.jpg', b'content', content_type='image/jpeg')
        p = Product(
            product_name='P2', slug='p2', description='d', price=1,
            images=img, stock=-5, category=self.category, created_by=self.user
        )
        with self.assertRaises(ValidationError):
            p.full_clean()


class ProductAPITests(TestCase):
    def setUp(self):
        # Setup temporary media root so uploads don't persist
        self._media_root = tempfile.mkdtemp()
        settings.MEDIA_ROOT = self._media_root

        self.client = APIClient()
        self.user = User.objects.create_user(username='owner2', password='pass')
        self.other = User.objects.create_user(username='other', password='pass')
        self.category = Category.objects.create(name='APIcat', slug='apicat')

    def tearDown(self):
        shutil.rmtree(self._media_root, ignore_errors=True)

    def _image(self):
        return SimpleUploadedFile('test.jpg', b'GIF87a', content_type='image/gif')

    def test_create_product_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'product_name': 'New',
            'slug': 'new',
            'description': 'desc',
            'price': '9.99',
            'stock': 10,
            'is_available': True,
            'category': self.category.id,
            'images': self._image(),
        }
        response = self.client.post('/api/products/', data, format='multipart')
        if response.status_code != 201:
            print('CREATE_RESPONSE:', response.content)
            self.fail('Product creation failed')
        self.assertEqual(Product.objects.count(), 1)
        prod = Product.objects.first()
        self.assertEqual(prod.created_by, self.user)

    def test_update_by_non_owner_forbidden(self):
        # create product as owner
        self.client.force_authenticate(user=self.user)
        data = {
            'product_name': 'Up',
            'slug': 'up',
            'description': 'desc',
            'price': '5.00',
            'stock': 2,
            'is_available': True,
            'category_id': self.category.id,
            'images': self._image(),
        }
        res = self.client.post('/api/products/', data, format='multipart')
        if res.status_code != 201:
            print('CREATE_RESPONSE:', res.content)
            self.fail('Product creation failed')
        prod_id = res.json().get('id')

        # try update as other user
        self.client.force_authenticate(user=self.other)
        upd = {'product_name': 'Hacked', 'category': self.category.id}
        res2 = self.client.patch(f'/api/products/{prod_id}/', upd, format='json')
        self.assertIn(res2.status_code, (403, 404))

    def test_owner_can_delete(self):
        self.client.force_authenticate(user=self.user)
        data = {
            'product_name': 'Del',
            'slug': 'del',
            'description': 'd',
            'price': '1.00',
            'stock': 1,
            'is_available': True,
            'category': self.category.id,
            'images': self._image(),
        }
        res = self.client.post('/api/products/', data, format='multipart')
        if res.status_code != 201:
            print('CREATE_RESPONSE:', res.content)
            self.fail('Product creation failed')
        prod_id = res.json().get('id')

        res2 = self.client.delete(f'/api/products/{prod_id}/')
        self.assertIn(res2.status_code, (204, 200))
from django.test import TestCase

# Create your tests here.
