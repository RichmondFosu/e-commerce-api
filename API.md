# E-commerce API Documentation

This API provides endpoints for managing products and categories in an e-commerce system. It uses Django REST Framework (DRF) for building the API.

## Base URL
`http://localhost:8000/api/`

## Authentication
The API uses token-based authentication. Obtain a token via `/api-auth/token/` or register/login at `/api/accounts/`.

Include the token in headers: `Authorization: Token <your-token>`

## Endpoints

### Accounts
- `POST /api/accounts/register/` - Register a new user
- `POST /api/accounts/login/` - Login and get token
- `POST /api/accounts/logout/` - Logout (invalidate token)

### Categories
- `GET /api/categories/` - List categories (public)
- `POST /api/categories/` - Create category (authenticated)
- `GET /api/categories/{id}/` - Retrieve category
- `PUT /api/categories/{id}/` - Update category (authenticated)
- `PATCH /api/categories/{id}/` - Partial update category (authenticated)
- `DELETE /api/categories/{id}/` - Delete category (authenticated)

Query parameters for categories:
- `search`: Search by name or description
- `name`, `slug`: Filter by name/slug
- `created_at_after`, `created_at_before`: Filter by date
- `ordering`: Sort by name or created_at

### Products
- `GET /api/products/` - List products (public)
- `POST /api/products/` - Create product (authenticated)
- `GET /api/products/{id}/` - Retrieve product
- `PUT /api/products/{id}/` - Update product (owner only)
- `PATCH /api/products/{id}/` - Partial update product (owner only)
- `DELETE /api/products/{id}/` - Delete product (owner only)

Query parameters for products:
- `search`: Search by product_name or description
- `category`: Filter by category slug
- `in_stock`: Filter by availability
- `min_price`, `max_price`: Filter by price range
- `ordering`: Sort by product_name, price, created_date
- `page`, `page_size`: Pagination

## Features
- **Filtering**: Use query parameters to filter results.
- **Search**: Full-text search on relevant fields.
- **Pagination**: Results are paginated; use `page` and `page_size`.
- **Permissions**: Read operations are public; write operations require authentication. Product edits/deletes are owner-only.

## Usage Examples

### Register User
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "email": "test@example.com", "password": "password123"}'
```

### Get Token
```bash
curl -X POST http://localhost:8000/api-auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "password123"}'
```

### List Products
```bash
curl http://localhost:8000/api/products/
```

### Create Product (Authenticated)
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token <your-token>" \
  -H "Content-Type: application/json" \
  -d '{"product_name": "New Product", "price": 10.99, "category_id": 1}'
```

### Filter Products
```bash
curl "http://localhost:8000/api/products/?category=electronics&min_price=10"
```

## Demo Web Interface
A web interface is available at `/demo/` for testing and browsing products/categories.
