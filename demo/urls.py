from django.urls import path
from .views import login_view, logout_view, product_list_view, product_add_view

app_name = 'demo'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('products/', product_list_view, name='product_list'),
    path('products/add/', product_add_view, name='product_add'),
]
