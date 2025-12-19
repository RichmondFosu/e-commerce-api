from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from products.filters import ProductFilter
from .models import Product
from .serializers import ProductSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import ProductCreateSerializer
from .models import ProductImage
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page


@method_decorator(cache_page(60 * 5), name='list')
class ProductViewSet(ModelViewSet):
    """
    Handles all CRUD operations for products.
    
    - Read operations: open to everyone
    - Write operations: restricted to authenticated users
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    filter_backends =   [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]

    filterset_class = ProductFilter  

    search_fields = ['product_name', 'description']

    # auto-assign the user who created the product
    def perform_create(self, serializer):
        # Save product and then handle any extra uploaded images
        product = serializer.save(created_by=self.request.user)
        # Handle extra images uploaded under `extra_images` (multipart list)
        files = self.request.FILES.getlist('extra_images') if hasattr(self.request, 'FILES') else []
        for f in files:
            ProductImage.objects.create(product=product, image=f)

    def get_serializer_class(self) -> type:
        # Use a write serializer for create/update, read serializer for others
        if self.action in ('create', 'update', 'partial_update'):
            return ProductCreateSerializer
        return super().get_serializer_class()


# Notes: `IsAuthenticatedOrReadOnly` allows public reads; write actions require auth.
# `IsOwnerOrReadOnly` restricts modifications to the creator of the product.


from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Product
from categories.models import Category
from .forms import ProductForm

# List products with search, filter, pagination (for template)
def product_list_view(request):
    products = Product.objects.all()
    categories = Category.objects.all()

    # Search
    search_query = request.GET.get('search')
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        products = products.filter(category_id=category_id)

    # Pagination
    paginator = Paginator(products, 6)  # 6 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {
        'page_obj': page_obj,
        'categories': categories
    })

# Product detail
def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'products/product_detail.html', {'product': product})

# Add product (authenticated)
@login_required
def product_add_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            product.created_by = request.user
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form})

# Edit product (authenticated & owner only)
@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.created_by != request.user:
        return redirect('product_detail', pk=pk)
    
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_detail', pk=pk)
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'product': product})

# Delete product (authenticated & owner only)
@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if product.created_by != request.user:
        return redirect('product_detail', pk=pk)
    
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    
    return render(request, 'products/product_confirm_delete.html', {'product': product})

