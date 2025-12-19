import django_filters
from .models import Category

class CategoryFilter(django_filters.FilterSet):
    # Case-insensitive partial match for name and slug
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    slug = django_filters.CharFilter(field_name='slug', lookup_expr='icontains')
    
    # filter categories by creation date range
    created_at = django_filters.DateFromToRangeFilter()

    class Meta:
        model = Category
        # Allow filtering by name, slug, and created_at
        fields = ['name', 'slug', 'created_at']
