from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name must be unique
    created_at = models.DateTimeField(auto_now_add=True)   # Auto-set creation timestamp
    slug = models.SlugField(unique=True, max_length=100,null=True)   # Slug for URL representation
    description = models.TextField(blank=True, null=True)  # Optional description field

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']  # Default ordering by name

    def __str__(self):
        return self.name  # For readable representation in admin and shell


# Model: Category
# Purpose: Store product categories (e.g., Electronics, Clothing)
# 'name' is unique to avoid duplicate categories
# 'created_at' auto-records when the category is created
# This model can be extended with additional fields as needed