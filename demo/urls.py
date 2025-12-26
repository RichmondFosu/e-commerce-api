from django.urls import path
from .views import landing_view, login_view, logout_view, product_list_view, product_add_view, product_detail_view, product_edit_view, product_delete_view, advanced_filter_view, presentation_view

app_name = 'demo'

urlpatterns = [
    path('', landing_view, name='landing'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('products/', product_list_view, name='product_list'),
    path('products/add/', product_add_view, name='product_add'),
    path('products/<int:product_id>/', product_detail_view, name='product_detail'),
    path('products/<int:product_id>/edit/', product_edit_view, name='product_edit'),
    path('products/<int:product_id>/delete/', product_delete_view, name='product_delete'),
    path('advanced-filter/', advanced_filter_view, name='advanced_filter'),
    path('presentation/', presentation_view, name='presentation'),
]
