from django.db import models
from categories.models import Category
from django.contrib.auth.models import User

# Create your models here.

class Product(models.Model):
    product_name        = models.CharField(max_length=255)
    slug                = models.SlugField(unique=True, max_length=255)
    description         = models.TextField()
    price               = models.DecimalField(max_digits=10, decimal_places=2)
    images              = models.ImageField(upload_to='photos/products', blank=True, null=True)  # Stores product images
    stock               = models.IntegerField()
    is_available        = models.BooleanField(default=True)
    category            = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date        = models.DateTimeField(auto_now_add=True)
    updated_date        = models.DateTimeField(auto_now=True)
    # Track which user created the product
    created_by          = models.ForeignKey(User, on_delete=models.CASCADE,related_name='products')


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

    def save(self, *args, **kwargs):
        # Auto-generate slug from product name if not provided
        from django.utils.text import slugify

        if not self.slug:
            base = slugify(self.product_name)[:200]
            slug = base
            counter = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


class ProductImage(models.Model):
    """Optional extra images for a product. Keeps original `Product.images` as
    the primary image for backward compatibility.
    """
    product = models.ForeignKey(Product, related_name='extra_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='photos/products')
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.product_name} ({self.id})"
