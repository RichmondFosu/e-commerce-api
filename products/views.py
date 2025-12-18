from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend

class ProductViewSet(ModelViewSet):
    """
    Handles all CRUD operations for products.
    
    - Read operations: open to everyone
    - Write operations: restricted to authenticated users
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    # auto-assign the user who created the product
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


''''
Authentication Behavior (Important):

IsAuthenticatedOrReadOnly

Meaning:

- Anyone can view products

- Only logged-in users can create, update, delete

IsOwnerOrReadOnly
Meaning:
- Only the user who created the product can modify or delete it
- Others can only view the product

'''


class ProductListAPIView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
    ]

    search_fields = ['name']
    filterset_fields = ['category']




