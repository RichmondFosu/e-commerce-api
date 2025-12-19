from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Category


class CategoryModelTests(TestCase):
    def test_create_category(self):
        c = Category.objects.create(name='C1', slug='c1')
        self.assertEqual(str(c), 'C1')
from django.test import TestCase

# Create your tests here.
