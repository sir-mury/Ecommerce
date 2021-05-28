from rest_framework import serializers
from .models import OrderItem,Orders
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    products = OrderItem.product
    # serializers.SerializerMethodField('get_product_details')
    product = ProductSerializer()

    # print('product:',products)

    class Meta:
        model = OrderItem
        fields = (
            'id',
            'product',
            'order',
            'quantity',
        )

    def get_product_details(self, products):
        serializer = ProductSerializer(
            products.objects.get(product=products.product), many=True)
        return serializer.data


class OrderSerializer(serializers.ModelSerializer):
    orderitems = OrderItemSerializer(many=True)
    user = serializers.SerializerMethodField('get_user_email')
    orders = Orders
    order_total = serializers.SerializerMethodField('get_order_total')
    order_items = serializers.SerializerMethodField('get_order_items')

    class Meta:
        model = Orders
        fields = (
            'id',
            'user',
            'is_delivery',
            'paid',
            'pick_up_type',
            'orderitems',
            'date_created',
            'order_total',
            'order_items',
        )

    def get_user_email(self, orders):
        user = orders.user.get_full_name()
        return user

    def get_order_total(self, orders):
        return orders.get_order_total

    def get_order_items(self, orders):
        return orders.get_order_items