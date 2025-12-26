# E-commerce API

A comprehensive Django REST API for managing an e-commerce platform with products and categories, featuring a web demo interface.

## Features
- **User Authentication**: Token-based authentication for secure API access
- **Product Management**: Full CRUD operations for products with image uploads
- **Category Management**: Organize products into categories
- **Advanced Filtering**: Filter by category, price range, availability, and more
- **Search Functionality**: Full-text search across product names and descriptions
- **Pagination**: Efficient handling of large product lists
- **Owner-based Permissions**: Users can only edit/delete their own products
- **Web Demo Interface**: User-friendly web interface for browsing and managing products

## Project Structure
```
e-commerce-api/
├── accounts/          # User authentication app
├── categories/        # Category management app
├── products/          # Product management app
├── demo/              # Web demo interface app
├── products_api/      # Main Django project settings
├── media/             # Uploaded product images
└── docs/              # API documentation
```

## Quick Start
1. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run Migrations**:
   ```bash
   python manage.py migrate
   ```

3. **Start Development Server**:
   ```bash
   python manage.py runserver
   ```

4. **Access the Application**:
   - **Landing Page**: http://127.0.0.1:8000/
   - **Products Demo**: http://127.0.0.1:8000/products/
   - **API Documentation**: http://127.0.0.1:8000/api/

## Demo Features
- Browse products with search and filtering
- View product details with images
- User registration and login
- Add, edit, and delete products (authenticated users only)
- Responsive design with Bootstrap

## API Endpoints
- `GET /api/products/` - List products (public)
- `POST /api/products/` - Create product (authenticated)
- `GET /api/categories/` - List categories (public)
- `POST /api/accounts/register/` - Register new user
- `POST /api/accounts/login/` - Login and get token

## Technologies Used
- **Backend**: Django 6.0, Django REST Framework
- **Database**: SQLite (development), PostgreSQL (production)
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Authentication**: Token-based authentication
- **Image Handling**: Pillow for image processing

## Presentation Preparation
This project demonstrates:
1. **RESTful API Design**: Clean, well-documented API endpoints
2. **Authentication & Authorization**: Secure user management
3. **Database Design**: Proper relationships and data integrity
4. **Web Interface**: User-friendly demo application
5. **Best Practices**: Code organization, testing, documentation

## API Documentation
See [API.md](API.md) for detailed endpoints, usage examples, and authentication instructions.


