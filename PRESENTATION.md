# E-commerce Product API Presentation

## Overview
This presentation covers the E-commerce Product API, a comprehensive Django REST Framework (DRF) based API for managing products and categories in an e-commerce platform. The project includes user authentication, product CRUD operations, advanced filtering, search, pagination, and a web demo interface for testing and browsing.

The API allows users to manage products with features like image uploads, category associations, and owner-based permissions. A key security feature is that products can only be edited and deleted by their created user, ensuring data integrity and user privacy. This owner-only restriction has been recently implemented and enforced in the permission system to prevent unauthorized modifications. It demonstrates best practices in RESTful API design, authentication, database relationships, and web interface integration.

## Technologies Used
- **Backend Framework**: Django 6.0 with Django REST Framework (DRF)
- **Database**: SQLite (for development), PostgreSQL (for production)
- **Authentication**: Token-based authentication using DRF's token auth
- **Filtering & Search**: django-filter and DRF filters for advanced querying
- **Pagination**: DRF pagination for efficient data handling
- **Image Handling**: Pillow for image processing and uploads
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript for the demo interface
- **HTTP Client**: Python requests library for API calls in the demo app

## Architecture
The project follows a modular Django app structure:

- **accounts/**: Handles user registration, login, logout, and token management
- **categories/**: Manages category CRUD operations with filtering and search
- **products/**: Core app for product management, including models, serializers, views, filters, and permissions
- **demo/**: Web interface app that interacts with the API via HTTP requests
- **products_api/**: Main Django project with settings, URLs, and configuration

Key architectural decisions:
- **Model-ViewSet Pattern**: Used for consistent CRUD operations
- **Owner-based Permissions**: Ensures users can only modify their own products
- **Separation of Concerns**: API logic separated from web interface
- **RESTful Design**: Clean, predictable endpoints with proper HTTP methods

## Key Endpoints and Functionalities

### Authentication Endpoints
- `POST /api/accounts/register/` - User registration
- `POST /api/accounts/login/` - User login and token retrieval
- `POST /api/accounts/logout/` - Token invalidation

### Category Endpoints
- `GET /api/categories/` - List all categories (public)
- `POST /api/categories/` - Create new category (authenticated)
- `GET /api/categories/{id}/` - Retrieve specific category
- `PUT /api/categories/{id}/` - Update category (authenticated)
- `DELETE /api/categories/{id}/` - Delete category (authenticated)

Query parameters: search, name, slug, created_at filters, ordering

### Product Endpoints
- `GET /api/products/` - List products with filtering and pagination (public)
- `POST /api/products/` - Create new product (authenticated)
- `GET /api/products/{id}/` - Retrieve product details
- `PUT /api/products/{id}/` - Update product (owner only)
- `DELETE /api/products/{id}/` - Delete product (owner only)

Query parameters: search, category, in_stock, min_price, max_price, ordering, page, page_size

## Authentication Process
The API uses token-based authentication:

1. **Registration**: Users register via `POST /api/accounts/register/` with username, email, password
2. **Login**: Users login via `POST /api/accounts/login/` to receive an authentication token
3. **API Access**: Include token in Authorization header: `Authorization: Token <token>`
4. **Logout**: Invalidate token via `POST /api/accounts/logout/`

Permissions:
- Read operations (GET) are public
- Write operations require authentication
- Product modifications are restricted to the owner

## Examples of Requests and Responses

### User Registration
**Request:**
```bash
curl -X POST http://localhost:8000/api/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_user", "email": "demo@example.com", "password": "securepass123"}'
```

**Response:**
```json
{
  "username": "demo_user",
  "email": "demo@example.com"
}
```

### Get Authentication Token
**Request:**
```bash
curl -X POST http://localhost:8000/api/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "demo_user", "password": "securepass123"}'
```

**Response:**
```json
{
  "token": "abc123def456..."
}
```

### List Products
**Request:**
```bash
curl http://localhost:8000/api/products/
```

**Response:**
```json
{
  "count": 25,
  "next": "http://localhost:8000/api/products/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "product_name": "Wireless Headphones",
      "price": 99.99,
      "stock": 50,
      "category": {
        "id": 1,
        "name": "Electronics"
      },
      "images": [
        {"image": "/media/photos/products/headphones.jpg"}
      ],
      "created_by": "demo_user"
    }
  ]
}
```

### Create Product
**Request:**
```bash
curl -X POST http://localhost:8000/api/products/ \
  -H "Authorization: Token abc123def456..." \
  -H "Content-Type: application/json" \
  -d '{
    "product_name": "New Laptop",
    "description": "High-performance laptop",
    "price": 1299.99,
    "stock": 10,
    "category_id": 1
  }'
```

**Response:**
```json
{
  "id": 26,
  "product_name": "New Laptop",
  "description": "High-performance laptop",
  "price": 1299.99,
  "stock": 10,
  "category": {
    "id": 1,
    "name": "Electronics"
  },
  "images": [],
  "created_by": "demo_user"
}
```

### Filter Products
**Request:**
```bash
curl "http://localhost:8000/api/products/?category=electronics&min_price=50&max_price=200&in_stock=true"
```

## Demo Features and API Interactions
The web demo interface demonstrates all API functionalities:

1. **Landing Page** (`/`): Introduction to the platform with navigation
2. **Product Browsing** (`/products/`): 
   - Displays paginated product list
   - Search bar for full-text search
   - Advanced filters (price range, category, stock status)
   - Links to product details
3. **Product Details** (`/products/{id}/`): 
   - Shows full product information and images
   - Edit/Delete buttons for owners
4. **User Authentication** (`/login/`): 
   - Login form that calls `/api/accounts/login/`
   - Registration link
5. **Product Management**:
   - Add Product form (`/products/add/`) - calls `POST /api/products/`
   - Edit Product (`/products/{id}/edit/`) - calls `PUT /api/products/{id}/`
   - Delete Product (`/products/{id}/delete/`) - calls `DELETE /api/products/{id}/`

All demo operations use the `requests` library to interact with the API, ensuring the web interface is a true client of the API.

## Web Interface Screenshots/Descriptions

### Landing Page
Clean, responsive landing page with Bootstrap styling. Features navigation bar, hero section introducing the platform, and quick links to browse products or login.

### Product List Page
Grid layout displaying products with images, names, prices, and categories. Includes:
- Search bar at the top
- "Advanced Filters" button revealing filter options
- Pagination controls at the bottom
- "Add Product" button for authenticated users

### Product Detail Page
Detailed view of a single product showing:
- Large product image(s)
- Full description, price, stock status
- Category information
- Edit/Delete buttons (visible only to product owner)

### Login Page
Simple form with username/password fields and submit button. Includes link to registration page.

### Add/Edit Product Page
Form with fields for product name, description, price, stock, category selection, and image upload. Uses multipart/form-data for file uploads.

## Conclusion
This E-commerce Product API project demonstrates:
- Robust RESTful API design with comprehensive CRUD operations
- Secure authentication and authorization mechanisms
- Advanced features like filtering, search, and pagination
- Proper separation between API and client interface
- Best practices in Django/DRF development
- User-friendly web demo for testing and demonstration

The project is production-ready with proper error handling, validations, and scalable architecture. It serves as an excellent foundation for building full e-commerce platforms.
