from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import CategorySerializer

class CategoryViewSet(ModelViewSet):
    """
    Handles all CRUD operations for product categories.

    - Read operations: open to everyone
    - Write operations: restricted to authenticated users
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
