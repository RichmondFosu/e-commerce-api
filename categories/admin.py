from django.contrib import admin
from .models import Category

# Custom admin class
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'created_at')  # Fields to show in admin list
    list_display_links = ('id','name')  # Make id and name clickable
    search_fields = ('name',)                    # Enable search by category name
    prepopulated_fields = {'slug': ('name',)}  # Auto-fill slug from name

# Register Category model with custom admin class
admin.site.register(Category, CategoryAdmin)