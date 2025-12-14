from django.db import models
from categories.models import Category

# Create your models here.

class Product(models.Model):
    product_name        = models.CharField(max_length=255)
    slug                = models.SlugField(unique=True, max_length=255)
    description         = models.TextField()
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    images              = models.ImageField(upload_to='photos/products')  # Stores product images
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    updated_date        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product_name

    #  model validation
    def clean(self):
        if self.price <= 0:
            from django.core.exceptions import ValidationError
            raise ValidationError({'price': 'Price must be greater than 0'})
        if self.stock < 0:
            from django.core.exceptions import ValidationError
            raise ValidationError({'stock': 'Stock cannot be negative'})
