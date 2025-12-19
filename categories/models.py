from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)  # Category name must be unique
    created_at = models.DateTimeField(auto_now_add=True)   # Auto-set creation timestamp
    slug = models.SlugField(unique=True, max_length=100, blank=True, null=True)   # Slug for URL representation
    description = models.TextField(blank=True, null=True)  # Optional description field

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        ordering = ['name']  # Default ordering by name

    def __str__(self):
        return self.name  # For readable representation in admin and shell

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        from django.utils.text import slugify

        if not self.slug:
            base = slugify(self.name)[:90]
            slug = base
            counter = 1
            while Category.objects.filter(slug=slug).exists():
                slug = f"{base}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)


# Model: Category
# Purpose: Store product categories (e.g., Electronics, Clothing)
# 'name' is unique to avoid duplicate categories
# 'created_at' auto-records when the category is created
# This model can be extended with additional fields as needed