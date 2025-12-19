# products/views.py
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .pagination import CustomPageNumberPagination
from .models import Product, ProductImage
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from .filters import ProductFilter

@method_decorator(cache_page(60 * 5), name='list')  # cache list view for 5 minutes
class ProductViewSet(ModelViewSet):
    """
    Handles all CRUD operations for products.

    - Read operations: open to everyone
    - Write operations: restricted to authenticated users
    - Modification restricted to product owner
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
    pagination_class = CustomPageNumberPagination

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['product_name', 'description']
    ordering_fields = ['product_name', 'price', 'created_date']
    ordering = ['product_name']

    def perform_create(self, serializer):
        """Assign the authenticated user as creator and handle extra images"""
        product = serializer.save(created_by=self.request.user)
        files = self.request.FILES.getlist('extra_images') if hasattr(self.request, 'FILES') else []
        for f in files:
            ProductImage.objects.create(product=product, image=f)
