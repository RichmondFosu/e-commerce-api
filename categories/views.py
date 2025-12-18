from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Category
from .serializers import CategorySerializer
from rest_framework import generics
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter 
from categories.filters import CategoryFilter


class CategoryListAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ["name"]


class CategoryViewSet(ModelViewSet):
    """
    Handles all CRUD operations for product categories.

    - Read operations: open to everyone
    - Write operations: restricted to authenticated users
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['name', 'description']
