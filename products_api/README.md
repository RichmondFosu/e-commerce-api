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
