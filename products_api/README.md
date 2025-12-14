# E-commerce API

**Project setup complete.** 

## Status:
- Django project created: `ecommerce_api`
- Products app created
- DRF installed and configured
- Initial migration applied
- Git repo initialized


## User Authentication Setup

- Django built-in User model used
- DRF authentication configured
- Login/logout endpoints available via `/api-auth/`
- Permissions set: authenticated users can modify products; read-only for others
- Concept focus: Authentication vs Authorization


## Category Model

- Category model created with fields: `name`, `created_at`
- `__str__` method added for readable representation
- Model registered in Django admin with search and list display
- Migrations applied successfully
- Purpose: Categories are independent entities for better product organization

## Product Model

- Product model created with fields:
  - product_name, slug, description, price, images, stock, is_available, category, created_date, updated_date

- Model linked to Category via ForeignKey

- Product registered in admin using ProductAdmin:
  - list_display shows key product fields
  - list_filter allows filtering by category, availability, and creation date
  - search_fields enables search by product_name, description, or slug
  
- Migrations applied successfully

## Serializers

- CategorySerializer created to control API input/output for categories
  - Fields: id, name, created_at
  - id and created_at are read-only
- ProductSerializer created for products
  - Nested CategorySerializer used to represent category details
  - Fields: id, product_name, slug, description, price, images, stock, is_available, category, created_date, updated_date
  - read_only_fields: id, created_date, updated_date
  - Optional field-level validation added for price (>0)
- Concept focus: Serializer = API contract


## Product CRUD Views

- Implemented ProductViewSet using DRF ModelViewSet
- Full CRUD operations enabled
- Write operations restricted to authenticated users
- API routes registered using DefaultRouter
- Concept focus: HTTP methods ↔ CRUD mapping

## Category CRUD Views

- Implemented CategoryViewSet using DRF ModelViewSet
- Full CRUD operations for categories
- Write operations restricted to authenticated users
- Routes registered using DRF DefaultRouter
- Categories now accessible via API
