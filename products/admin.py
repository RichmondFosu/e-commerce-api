from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'product_name', 'category', 'price', 'stock', 'is_available', 'created_date')
    list_display_links = ('id', 'product_name', 'category')
    list_filter = ('category', 'is_available', 'created_date')
    search_fields = ('product_name', 'description', 'slug')
    ordering = ('-created_date',)
    prepopulated_fields = {'slug': ('product_name',)}

admin.site.register(Product, ProductAdmin)
    