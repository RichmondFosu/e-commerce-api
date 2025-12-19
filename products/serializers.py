from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer  # for nested representation
from categories.models import Category
from .models import ProductImage


class ProductSerializer(serializers.ModelSerializer):
    # Read: nested category object
    category = CategorySerializer(read_only=True)
    # Include extra images (many) in read responses
    extra_images = serializers.SerializerMethodField()

    # Write: accept category by its ID under `category_id`
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True, required=True
    )

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'description', 'price',
            'images', 'stock', 'is_available', 'category', 'category_id', 'extra_images',
            'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value

    def to_representation(self, instance):
        """Return product representation with absolute image URLs when request present."""
        data = super().to_representation(instance)
        request = self.context.get('request') if hasattr(self, 'context') else None
        # main image
        img = data.get('images')
        if img and request:
            try:
                data['images'] = request.build_absolute_uri(instance.images.url) if instance.images else None
            except Exception:
                data['images'] = img

        # extra images are already provided as dicts; ensure absolute URLs
        extras = data.get('extra_images')
        if extras and request:
            for e, obj in zip(extras, instance.extra_images.all()):
                if obj.image:
                    e['image'] = request.build_absolute_uri(obj.image.url)

        return data

    def get_extra_images(self, obj):
        imgs = obj.extra_images.all()
        return [
            {'id': i.id, 'image': i.image.url if i.image else None, 'created_date': i.created_date}
            for i in imgs
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    # Accept category as PK on write
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    images = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = Product
        fields = [
            'id', 'product_name', 'slug', 'description', 'price',
            'images', 'stock', 'is_available', 'category',
            'created_date', 'updated_date'
        ]
        read_only_fields = ['id', 'created_date', 'updated_date']

    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than 0")
        return value

    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("Stock cannot be negative")
        return value


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'created_date']

    def to_representation(self, instance):
        request = self.context.get('request') if hasattr(self, 'context') else None
        image_url = instance.image.url if instance.image else None
        if image_url and request:
            image_url = request.build_absolute_uri(image_url)
        return {
            'id': instance.id,
            'image': image_url,
            'created_date': instance.created_date,
        }

# (helper was moved into ProductSerializer)
