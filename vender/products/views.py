from products.models import Product
from products.serializers import ProductSerializer
from rest_framework import generics
from django.contrib.auth.models import User
from products.serializers import UserSerializer
from rest_framework import permissions
from products.permissions import IsOwnerOrReadOnly
from django.test import Client
from rest_framework.test import APIClient
from rest_framework.decorators import api_view

class ProductList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      IsOwnerOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(["POST"])
def ProductDelete(request):
    client = APIClient()
    client.login(username=request.data.get("email"),password=request.data.get("password"))

    path = '/products/' + request.data.get("product_id") + '/'
    response = client.delete(path)

    return response
