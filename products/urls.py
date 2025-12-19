from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet
from products.views_auth import RegisterAPIView

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')

urlpatterns = router.urls


urlpatterns += [
    path('api-auth/register/', RegisterAPIView.as_view(), name='register'),
]
