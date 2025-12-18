

## 🔍 Search and Filtering System

This API implements **search and filtering functionality** using **Django REST Framework (DRF) built-in filter backends** in combination with **django-filter**.
This approach follows best practices for building scalable and maintainable RESTful APIs.

---

### 📌 Technologies Used

* **Django REST Framework (DRF)**
* **django-filter**
* **DRF SearchFilter**
* **DRF DjangoFilterBackend**

These tools allow flexible querying of product data using URL query parameters without writing custom query logic.

---

## 🛠️ Configuration Overview

The API uses the following DRF filter backends:

* `SearchFilter` → for partial text search
* `DjangoFilterBackend` → for exact field-based filtering

They are enabled either globally in `settings.py` or locally at the view level.

---

## 🔎 Search Functionality

### Searchable Fields

* **Product name**

The search uses **partial matching** (case-insensitive), meaning it will return results that *contain* the search term.

### Example Usage

```http
GET /api/products/?search=laptop
```

This will return all products whose name includes:

* `Laptop`
* `Gaming Laptop`
* `Laptop Pro`

No exact match is required.

---

## 🏷️ Filtering Functionality

### Filterable Fields

* **Category**

Filtering allows clients to retrieve products belonging to a specific category.

### Example Usage

```http
GET /api/products/?category=electronics
```

This returns all products with the category `electronics`.

> If `category` is implemented as a ForeignKey, filtering is handled using related fields internally.

---

## 🔄 Combined Queries (Search + Filter)

Search and filtering can be combined in a single request to create flexible queries.

### Example

```http
GET /api/products/?search=phone&category=electronics
```

This returns:

* Products whose name contains **“phone”**
* AND belong to the **electronics** category

---

## 📋 Default Behavior

* If **no query parameters** are provided, the API returns **all products**
* If a query returns **no matches**, the API responds with:

  * HTTP `200 OK`
  * An empty list (`[]`)
* Invalid filters do **not** crash the API

---

## ✅ Why This Approach Was Chosen

Using DRF’s built-in filtering system provides:

* Clean and readable code
* Better performance and scalability
* Industry-standard API behavior
* Easy extension (ordering, pagination, advanced filters)

This makes the API suitable for:

* E-commerce platforms
* Inventory management systems
* Third-party API consumption

---

## 🚀 Extensibility

The current search and filtering system can easily be extended to support:

* Ordering (`?ordering=price`)
* Pagination
* Advanced filters (price range, availability, date added)

