from django.contrib.auth.models import User
from catalog.models import Category, CatalogItem
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'url']

class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CatalogItemSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CatalogItem
        fields = '__all__'
