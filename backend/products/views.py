from django.shortcuts import render
from rest_framework import generics
from rest_framework import status
from rest_framework import permissions
from rest_framework.permissions import IsAuthenticatedOrReadOnly, BasePermission
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
import datetime
from .models import Product, Tag, Category
from .serializers import ProductSerializer, TagSerializer, CategorySerializer
# Create your views here.



class ProductList(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class ProductDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]


class CategoryList(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()
