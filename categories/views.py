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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Category
from .forms import CategoryForm

# List categories
def category_list_view(request):
    categories = Category.objects.all()

    # Search
    search_query = request.GET.get('search')
    if search_query:
        categories = categories.filter(name__icontains=search_query)

    # Pagination (optional, 6 per page)
    from django.core.paginator import Paginator
    paginator = Paginator(categories, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'categories/category_list.html', {
        'categories': page_obj
    })


# Category detail
def category_detail_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    return render(request, 'categories/category_detail.html', {'category': category})


# Add category (authenticated users only)
@login_required
def category_add_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('category_list')
    else:
        form = CategoryForm()
    return render(request, 'categories/category_form.html', {'form': form})


# Edit category (authenticated users only)
@login_required
def category_edit_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect('category_detail', pk=category.pk)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'categories/category_form.html', {'form': form, 'category': category})


# Delete category (authenticated users only)
@login_required
def category_delete_view(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.method == 'POST':
        category.delete()
        return redirect('category_list')
    return render(request, 'categories/category_confirm_delete.html', {'category': category})
