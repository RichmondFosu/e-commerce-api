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


# **E-Commerce API Documentation**

**Base URL:** `http://localhost:8000/api/`

---

## **1. Products**

### **1.1 List Products (Paginated)**

* **Endpoint:** `GET /products/`
* **Description:** Returns a paginated list of all products.
* **Query Parameters:**

  * `page` (optional): Page number
  * `page_size` (optional): Number of items per page

**Example Request:**

```http
GET /api/products/?page=1&page_size=5
```

**Example Response:**

```json
{
  "count": 23,
  "next": "http://localhost:8000/api/products/?page=2&page_size=5",
  "previous": null,
  "results": [
    {"id": 1, "name": "T-Shirt", "price": 20, "category": "Clothing"},
    {"id": 2, "name": "Sneakers", "price": 50, "category": "Footwear"}
  ]
}
```

---

### **1.2 Retrieve Product**

* **Endpoint:** `GET /products/{id}/`
* **Description:** Get details of a single product by ID.

**Example Request:**

```http
GET /api/products/1/
```

**Example Response:**

```json
{
  "id": 1,
  "name": "T-Shirt",
  "price": 20,
  "description": "100% cotton",
  "category": "Clothing"
}
```

---

### **1.3 Create Product**

* **Endpoint:** `POST /products/`
* **Description:** Add a new product.

**Request Body:**

```json
{
  "name": "Hat",
  "price": 15,
  "description": "Stylish summer hat",
  "category": "Accessories"
}
```

**Response:** `201 Created`

---

### **1.4 Update Product**

* **Endpoint:** `PUT /products/{id}/` or `PATCH /products/{id}/`
* **Description:** Update product details.

**Example Request (PATCH):**

```http
PATCH /api/products/24/
```

```json
{
  "price": 18
}
```

---

### **1.5 Delete Product**

* **Endpoint:** `DELETE /products/{id}/`
* **Description:** Remove a product by ID.
* **Response:** `204 No Content`

---

### **1.6 Search Products**

* **Endpoint:** `GET /products/?search=<query>`
* **Description:** Search products by name or description. Pagination applies.

**Example Request:**

```http
GET /api/products/?search=shirt&page=1&page_size=5
```

---

### **1.7 Filter Products**

* **Endpoint:** `GET /products/?category=<category_name>&min_price=<min>&max_price=<max>`
* **Description:** Filter products by category and/or price range.

**Example Request:**

```http
GET /api/products/?category=Clothing&min_price=10&max_price=30
```

---

## **2. Orders**

### **2.1 List Orders (Paginated)**

* **Endpoint:** `GET /orders/`
* **Description:** Returns all orders in a paginated format.

**Example Request:**

```http
GET /api/orders/?page=1&page_size=5
```

---

### **2.2 Retrieve Order**

* **Endpoint:** `GET /orders/{id}/`
* **Description:** Get details of a specific order.

**Example Request:**

```http
GET /api/orders/1/
```

---

### **2.3 Create Order**

* **Endpoint:** `POST /orders/`
* **Request Body Example:**

```json
{
  "user": "john_doe",
  "products": [1, 5, 7],
  "status": "pending"
}
```

---

### **2.4 Update Order**

* **Endpoint:** `PATCH /orders/{id}/`
* **Example Request:**

```json
{
  "status": "completed"
}
```

---

### **2.5 Delete Order**

* **Endpoint:** `DELETE /orders/{id}/`
* **Response:** `204 No Content`

---

### **3. Tips for Users Testing**

1. Use query parameters to test **pagination**: `?page=2&page_size=5`
2. Test **search**: `?search=<keyword>`
3. Test **filtering**: `?category=Clothing&min_price=10&max_price=30`
4. Use **Postman**, **cURL**, or your browser for **GET requests**, and **Postman/cURL** for **POST, PATCH, DELETE**.

