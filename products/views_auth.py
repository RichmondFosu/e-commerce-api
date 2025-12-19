from rest_framework import generics
from products.serializers_auth import UserRegisterSerializer

class RegisterAPIView(generics.CreateAPIView):
    serializer_class = UserRegisterSerializer
