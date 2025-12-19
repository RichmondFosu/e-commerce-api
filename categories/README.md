# Categories App

The **Categories app** is part of the e-commerce API project. It manages **product categories** and exposes **CRUD operations** via Django REST Framework (DRF). The API supports **filtering, searching, and ordering** for easy integration with any frontend or API client.

---

## **Features**

* **CRUD Operations**: Create, retrieve, update, and delete categories.
* **Permissions**:

  * Read operations (list/retrieve) are open to everyone.
  * Write operations (create/update/delete) require authentication.
* **Filtering**: Filter by `name`, `slug`, and `created_at` (supports partial and case-insensitive matches).
* **Search**: Search categories by `name` or `description`.
* **Ordering**: Sort results by `name` or `created_at`.

---

## **How It Works**

* **API Endpoint**: `/api/categories/`
* Uses a **ModelViewSet** with DRF, so all CRUD operations are available at standard REST endpoints.
* **Filtering** is handled via `django_filters` and the custom `CategoryFilter`.
* **Search and ordering** are handled via DRF’s `SearchFilter` and `OrderingFilter`.

---

## **How to Try It**

1. **Run the server**:

```bash
python manage.py runserver
```

2. **List categories**:

```
GET /api/categories/
```

3. **Search categories**:

```
GET /api/categories/?search=electronics
```

4. **Filter categories**:

```
GET /api/categories/?name=elec&slug=elec
GET /api/categories/?created_at_after=2025-01-01&created_at_before=2025-12-31
```

5. **Order categories**:

```
GET /api/categories/?ordering=-created_at
```

6. **Create a category** (requires authentication token):

```json
POST /api/categories/
Authorization: Token <your-token>
{
  "name": "Electronics",
  "description": "Electronic gadgets and devices",
  "slug": "electronics"
}
```

7. **Update or delete a category** also requires authentication and uses standard `PUT`, `PATCH`, or `DELETE` HTTP methods.

---

## **Notes**

* The app is **API-first**; no HTML templates are included.
* It works seamlessly with the **accounts app** for authenticated operations.
* Can be extended to include **nested products**, additional filters, or more advanced search features.

---

