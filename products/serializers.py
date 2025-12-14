from rest_framework import serializers
from .models import Product
from categories.serializers import CategorySerializer  # for nested representation
from categories.models import Category

class ProductSerializer(serializers.ModelSerializer):
    # Show category as nested object
    category = CategorySerializer(read_only=True)
    
    # Accept category by ID
    # category_id = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), source='category')

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