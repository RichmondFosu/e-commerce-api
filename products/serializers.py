# products/serializers.py
from rest_framework import serializers
from .models import Product, ProductImage
from categories.models import Category
from categories.serializers import CategorySerializer

# Helper for DRY validation
def validate_positive(value, field_name):
    if value <= 0:
        raise serializers.ValidationError(f"{field_name} must be greater than 0")
    return value

class ProductSerializer(serializers.ModelSerializer):
    # Nested category object for read
    category = CategorySerializer(read_only=True)
    # Accept category by ID for write
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=True
    )
    # Extra images included in read responses
    extra_images = serializers.SerializerMethodField()
    # Images field handled in to_representation for absolute URLs
    # Include creator username
    created_by = serializers.CharField(source='created_by.username', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'description', 'price',
            'images', 'stock', 'is_available', 'category', 'category_id',
            'extra_images', 'created_date', 'updated_date', 'created_by'
        ]
        read_only_fields = ['id', 'slug', 'created_date', 'updated_date', 'created_by']

    # Validations
    def validate_price(self, value):
        return validate_positive(value, 'Price')

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value

    # Extra images representation
    def get_extra_images(self, obj):
        request = self.context.get('request')
        return [
            {
                'id': img.id,
                'image': request.build_absolute_uri(img.image.url) if img.image and request else img.image.url if img.image else None,
                'created_date': img.created_date
            }
            for img in obj.extra_images.all()
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return data

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_date']

    def to_representation(self, instance):
        request = self.context.get('request')
        image_url = instance.image.url if instance.image else None
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)
        return {
            'id': instance.id,
            'image': image_url,
            'created_date': instance.created_date
        }
