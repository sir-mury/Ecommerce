from django.urls import path
from .views import OrdersDetailView,CartView,AddToCartView #ProcessOrderView,CheckOutView,


urlpatterns = [
    path('orders/', OrdersDetailView.as_view(), name='orders'),
    path('cart/', CartView.as_view(), name='cart'),
    #path('process-order/', ProcessOrderView.as_view(), name='process-order'),
    #path('orders/<int:pk>/',OrdersDetail.as_view(),name='orders detail'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    #path('checkout/', CheckOutView.as_view(), name='checkout'),
]