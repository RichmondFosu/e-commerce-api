# Accounts App

The **Accounts app** handles **user registration, login, and logout** for the e-commerce API. It uses **Django REST Framework Token Authentication** to secure the API, allowing only authenticated users to perform certain actions like creating, updating, or deleting categories and products.

---

## How It Works

* **Register:** Users can create an account by sending their username, email, and password.
* **Login:** Registered users receive an **authentication token** to use for API requests.
* **Logout:** Users can invalidate their token, preventing further access until they log in again.
* **Token Authentication:** API endpoints check the token to allow or restrict access.

---

## How to Try It

1. **Run the server**:

```bash
python manage.py runserver
```

2. **Register a user**:

```http
POST /api/accounts/register/
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

3. **Login to get token**:

```http
POST /api/accounts/login/
{
  "username": "john",
  "password": "password123"
}
```

Response:

```json
{
  "token": "your-auth-token",
  "user_id": 1,
  "username": "john"
}
```

4. **Use token for authenticated requests**:

```
Authorization: Token your-auth-token
```

5. **Logout**:

```
POST /api/accounts/logout/
Authorization: Token your-auth-token
```

---

This is **all you need** to create users, log in, and secure API operations.

---
