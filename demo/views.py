# demo/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
import requests

API_TOKEN_URL = 'http://127.0.0.1:8000/api/accounts/login/'
API_BASE_URL = 'http://127.0.0.1:8000/api/'

def landing_view(request):
    # Fetch products and categories for unauthenticated users
    params = {
        'search': request.GET.get('search', ''),
        'category': request.GET.get('category', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'in_stock': request.GET.get('in_stock', ''),
        'page': request.GET.get('page', 1),
    }

    try:
        response = requests.get(f"{API_BASE_URL}products/", params=params)
        categories_resp = requests.get(f"{API_BASE_URL}categories/")
    except requests.exceptions.ConnectionError:
        messages.error(request, "Cannot connect to API. Make sure server is running.")
        return render(request, 'demo/landing.html', {'products': [], 'data': {}})

    if response.status_code != 200:
        messages.error(request, "Failed to load products.")
        products = []
        data = {}
    else:
        data = response.json()
        products = data.get('results', data)

        # Extract page numbers from pagination URLs
        if data.get('next'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(data['next'])
            params = parse_qs(parsed.query)
            data['next_page'] = params.get('page', [None])[0]
        if data.get('previous'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(data['previous'])
            params = parse_qs(parsed.query)
            data['previous_page'] = params.get('page', [None])[0]

    # Fetch categories for the dropdown
    categories = []
    if categories_resp.status_code == 200:
        categories = categories_resp.json()
    else:
        messages.warning(request, "Failed to load categories.")

    # Add categories to data for template
    data['categories'] = categories

    return render(request, 'demo/landing.html', {
        'products': products,
        'data': data,
        'categories': categories,
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            response = requests.post(
                API_TOKEN_URL,
                data={'username': username, 'password': password}
            )
        except requests.exceptions.ConnectionError:
            messages.error(request, "Cannot connect to API. Make sure server is running.")
            return render(request, 'demo/login.html')

        if response.status_code == 200:
            token = response.json().get('token')
            request.session['token'] = token
            return redirect('demo:product_list')
        else:
            messages.error(request, f'Invalid credentials or API error ({response.status_code}).')

    return render(request, 'demo/login.html')


def logout_view(request):
    request.session.pop('token', None)
    return redirect('demo:login')


def product_list_view(request):
    token = request.session.get('token')
    headers = {}
    if token:
        headers['Authorization'] = f'Token {token}'

    params = {
        'search': request.GET.get('search', ''),
        'category': request.GET.get('category', ''),
        'min_price': request.GET.get('min_price', ''),
        'max_price': request.GET.get('max_price', ''),
        'in_stock': request.GET.get('in_stock', ''),
        'page': request.GET.get('page', 1),
    }

    try:
        response = requests.get(f"{API_BASE_URL}products/", headers=headers, params=params)
        categories_resp = requests.get(f"{API_BASE_URL}categories/", headers=headers)
    except requests.exceptions.ConnectionError:
        messages.error(request, "Cannot connect to API. Make sure server is running.")
        return render(request, 'demo/product_list.html', {'products': [], 'data': {}})

    if response.status_code != 200:
        messages.error(request, "Failed to load products.")
        products = []
        data = {}
    else:
        data = response.json()
        products = data.get('results', data)

        # Extract page numbers from pagination URLs
        if data.get('next'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(data['next'])
            params = parse_qs(parsed.query)
            data['next_page'] = params.get('page', [None])[0]
        if data.get('previous'):
            from urllib.parse import urlparse, parse_qs
            parsed = urlparse(data['previous'])
            params = parse_qs(parsed.query)
            data['previous_page'] = params.get('page', [None])[0]

    # Fetch categories for the dropdown
    categories = []
    if categories_resp.status_code == 200:
        categories = categories_resp.json()
    else:
        messages.warning(request, "Failed to load categories.")

    # Add categories to data for template
    data['categories'] = categories

    return render(request, 'demo/product_list.html', {
        'products': products,
        'data': data,
        'categories': categories,
    })



PRODUCTS_API_URL = f"{API_BASE_URL}products/"
CATEGORIES_API_URL = f"{API_BASE_URL}categories/"

def product_detail_view(request, product_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, "You must be logged in to view product details.")
        return redirect('demo:login')

    headers = {}
    if token:
        headers['Authorization'] = f'Token {token}'

    try:
        response = requests.get(f"{PRODUCTS_API_URL}{product_id}/", headers=headers)
    except requests.exceptions.ConnectionError:
        messages.error(request, "Cannot connect to API. Make sure server is running.")
        return redirect('demo:product_list')

    if response.status_code == 200:
        product = response.json()
        return render(request, 'demo/product_detail.html', {'product': product})
    else:
        messages.error(request, f"Failed to load product. ({response.status_code})")
        return redirect('demo:product_list')


def product_edit_view(request, product_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, "You must be logged in to edit a product.")
        return redirect('demo:login')

    headers = {'Authorization': f'Token {token}'}

    # Fetch categories
    categories_resp = requests.get(CATEGORIES_API_URL, headers=headers)
    categories = categories_resp.json() if categories_resp.status_code == 200 else []

    if request.method == 'POST':
        data = {
            'product_name': request.POST.get('product_name'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'stock': request.POST.get('stock'),
            'category_id': request.POST.get('category'),
            'is_available': True,
        }

        files = {}
        if request.FILES.get('images'):
            files['images'] = request.FILES['images']

        extra_files = request.FILES.getlist('extra_images')
        for i, f in enumerate(extra_files):
            files[f'extra_images[{i}]'] = f

        response = requests.put(
            f"{PRODUCTS_API_URL}{product_id}/",
            headers=headers,
            data=data,
            files=files
        )

        if response.status_code == 200:
            messages.success(request, "Product updated successfully.")
            return redirect('demo:product_list')
        else:
            messages.error(request, f"Failed to update product. ({response.status_code})")
            print(response.text)

    # GET request - fetch current product data
    try:
        response = requests.get(f"{PRODUCTS_API_URL}{product_id}/", headers=headers)
    except requests.exceptions.ConnectionError:
        messages.error(request, "Cannot connect to API. Make sure server is running.")
        return redirect('demo:product_list')

    if response.status_code == 200:
        product = response.json()
        return render(request, 'demo/product_edit.html', {'product': product, 'categories': categories})
    else:
        messages.error(request, f"Failed to load product. ({response.status_code})")
        return redirect('demo:product_list')


def product_delete_view(request, product_id):
    token = request.session.get('token')
    if not token:
        messages.error(request, "You must be logged in to delete a product.")
        return redirect('demo:login')

    headers = {'Authorization': f'Token {token}'}

    if request.method == 'POST':
        response = requests.delete(f"{PRODUCTS_API_URL}{product_id}/", headers=headers)

        if response.status_code == 204:
            messages.success(request, "Product deleted successfully.")
        else:
            messages.error(request, f"Failed to delete product. ({response.status_code})")

        return redirect('demo:product_list')

    # GET request - show confirmation
    try:
        response = requests.get(f"{PRODUCTS_API_URL}{product_id}/", headers=headers)
    except requests.exceptions.ConnectionError:
        messages.error(request, "Cannot connect to API. Make sure server is running.")
        return redirect('demo:product_list')

    if response.status_code == 200:
        product = response.json()
        return render(request, 'demo/product_delete.html', {'product': product})
    else:
        messages.error(request, f"Failed to load product. ({response.status_code})")
        return redirect('demo:product_list')

def product_add_view(request):
    token = request.session.get('token')
    if not token:
        messages.error(request, "You must be logged in to add a product.")
        return redirect('demo:login')

    # Fetch categories from API to populate the dropdown
    headers = {'Authorization': f'Token {token}'}
    categories_resp = requests.get(CATEGORIES_API_URL, headers=headers)
    categories = categories_resp.json() if categories_resp.status_code == 200 else []

    if request.method == 'POST':
        # Gather form data
        data = {
            'product_name': request.POST.get('product_name'),
            'description': request.POST.get('description'),
            'price': request.POST.get('price'),
            'stock': request.POST.get('stock'),
            'category_id': request.POST.get('category'),
            'is_available': True,
        }

        files = {}
        # Main image
        if request.FILES.get('images'):
            files['images'] = request.FILES['images']

        # Extra images (multiple)
        extra_files = request.FILES.getlist('extra_images')
        for i, f in enumerate(extra_files):
            files[f'extra_images[{i}]'] = f

        # Send POST request to DRF API
        response = requests.post(
            PRODUCTS_API_URL,
            headers=headers,
            data=data,
            files=files
        )

        if response.status_code in (200, 201):
            messages.success(request, "Product added successfully.")
            return redirect('demo:product_list')
        else:
            messages.error(request, f"Failed to add product. ({response.status_code})")
            print(response.text)  # Debug API response

    return render(request, 'demo/product_add.html', {'categories': categories})

def advanced_filter_view(request):
    # Fetch categories for the dropdown
    try:
        categories_resp = requests.get(f"{API_BASE_URL}categories/")
    except requests.exceptions.ConnectionError:
        messages.error(request, "Cannot connect to API. Make sure server is running.")
        return render(request, 'demo/advanced_filter.html', {'categories': []})

    categories = []
    if categories_resp.status_code == 200:
        categories = categories_resp.json()
    else:
        messages.warning(request, "Failed to load categories.")

    if request.method == 'POST':
        # Build query parameters from form
        params = {
            'search': request.POST.get('search', ''),
            'category': request.POST.get('category', ''),
            'min_price': request.POST.get('min_price', ''),
            'max_price': request.POST.get('max_price', ''),
            'in_stock': request.POST.get('in_stock', ''),
        }
        # Remove empty parameters
        params = {k: v for k, v in params.items() if v}

        # Redirect to product list with filters
        from urllib.parse import urlencode
        query_string = urlencode(params)
        return redirect(f"{reverse('demo:product_list')}?{query_string}")

    return render(request, 'demo/advanced_filter.html', {'categories': categories})

def presentation_view(request):
    """View for the API operations presentation page."""
    return render(request, 'demo/presentation.html')
