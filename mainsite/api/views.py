from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework import permissions
from catalog.models import CatalogItem, Category
from api.serializers import UserSerializer, CatalogItemSerializer, CategorySerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class CatalogItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = CatalogItem.objects.all().order_by('-date_added')
    serializer_class = CatalogItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
