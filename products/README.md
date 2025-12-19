# Products App

## **Overview**

The **Products app** is part of an e-commerce API project. It manages all product-related operations, including creating, reading, updating, and deleting products.

Key features:

* CRUD operations for products
* Product categorization using the **Categories app**
* Supports product images, including multiple extra images per product
* Filtering, searching, and ordering of products
* Pagination for API endpoints
* Permissions: public read, write restricted to authenticated users, edits restricted to product owner

---

## **How It Works**

1. **Product Model**

   * `product_name`, `slug`, `description`, `price`, `stock`, `is_available`
   * Primary image stored in `images` field
   * Optional extra images in `ProductImage` model
   * Linked to a **Category** and tracks which user created it (`created_by`)

2. **Serializers**

   * `ProductSerializer` handles both read and write operations

     * Returns nested category data and extra images for read
     * Accepts `category_id` for write
   * `ProductImageSerializer` returns image URLs with absolute paths

3. **Views / API**

   * `ProductViewSet` provides all CRUD endpoints via DRF `ModelViewSet`
   * Permissions:

     * Public read access
     * Authenticated users can create
     * Only owners can update or delete their products
   * Filtering, searching, and ordering supported:

     * Filter by `category` slug, `in_stock`, `min_price`, `max_price`
     * Search by `product_name` or `description`
     * Ordering by `product_name`, `price`, `created_date`
   * Pagination: configurable page size with maximum 100 items per page

4. **Custom Permissions**

   * `IsOwnerOrReadOnly` ensures only the product creator can modify or delete the product

---

## **API Endpoints**

Assuming your base URL is `/api/`:

| Endpoint          | Method | Description                                   |
| ----------------- | ------ | --------------------------------------------- |
| `/products/`      | GET    | List all products (supports filtering/search) |
| `/products/`      | POST   | Create a new product (auth required)          |
| `/products/{id}/` | GET    | Retrieve a single product                     |
| `/products/{id}/` | PUT    | Update a product (owner only)                 |
| `/products/{id}/` | PATCH  | Partially update a product (owner only)       |
| `/products/{id}/` | DELETE | Delete a product (owner only)                 |

**Filtering Example:**

```
GET /products/?min_price=10&max_price=100&in_stock=true&category=electronics
```

**Pagination Example:**

```
GET /products/?page=2&page_size=10
```

---

## **How to Try**

1. **Run Migrations**

```bash
python manage.py makemigrations
python manage.py migrate
```

2. **Create a Superuser / Test Users**

```bash
python manage.py createsuperuser
```

3. **Run Development Server**

```bash
python manage.py runserver
```

4. **Test API Endpoints**

   * Use Postman, cURL, or a browser (for GET endpoints)
   * Include authentication token (if using DRF authtoken) for write operations

5. **Upload Products**

   * Include `category_id` when creating a product
   * Extra images can be uploaded via `multipart/form-data` under `extra_images`

---

## **Notes**

* Works best with the **Categories app** for proper product categorization.
* Designed for an **API-first architecture**; template views are optional and not required.
* Integrates with **Accounts app** for authentication and user management.

---