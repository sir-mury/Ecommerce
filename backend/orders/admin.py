from django.contrib import admin
from .models import OrderItem,Orders
# Register your models here.


@admin.register(Orders)
class OrdersAdmin(admin.ModelAdmin):
    list_display = ['user','paid','date_created']
    search_fields = ['user']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['product','quantity','orders']
    search_fields = ['name']
    list_editable = ['quantity']