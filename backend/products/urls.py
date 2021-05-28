from django.urls import path
from .views import ProductList, ProductDetail

urlpatterns = [
    path('products/', ProductList.as_view(), name='Products'),
    path('products/<int:pk>/', ProductDetail.as_view(), name='Product Detail'),
]
