from products.models import Product
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from .serializers import OrderItemSerializer,OrderSerializer
from .models import Orders,OrderItem
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import permissions
# Create your views here.

class IsUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        # elif request.method in permissions.SAFE_METHODS:
        #     return False
        elif obj.user != request.user:
            return False
        else:
            return False


class OrdersDetailView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        orders = Orders.objects.filter(user=request.user)
        serializer = OrderSerializer(orders,many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class CartView(APIView):
    permission_classes = [IsUser]

    def get(self, request):
        orders = Orders.objects.filter(user=request.user, cart=True)
        print("User:", request.user)
        serializer = OrderSerializer(orders[0])
        return Response(serializer.data, status=HTTP_200_OK)

# class OrdersList(generics.ListAPIView):
#     permission_classes = [IsUser]
#     serializer_class = OrderSerializer
#     queryset = Orders.objects.all()


class AddToCartView(APIView):
    def post(self, request, *args, **kwargs):
        permission_classes = [IsUser]
        id = request.data['id']
        action = request.data['action']
        if id or action is None:
            return Response({"message": "Invalid Request"}, status=HTTP_400_BAD_REQUEST)
        product = generics.get_object_or_404(Product, id=id)
        order, created = Orders.objects.get_or_create(user=request.user)
        order_item, created = OrderItem.objects.get_or_create(
            product=product,
            order=order
        )

        if action == 'add':
            order_item.quantity += 1
            return Response({"message": "Product updated successfully"}, status=HTTP_200_OK)
        elif action == 'remove':
            order_item.quantity -= 1
            return Response({"message": "Product removed successfully"}, status=HTTP_200_OK)
        print('OrderItem:', order_item)

        order_item.save()

        if order_item.quantity <= 0:
            order_item.delete()


# class CheckOutView(APIView):
#     def get(self, request):
#         permission_classes = [IsUser]
#         order_items = OrderItem.objects.filter(order=request.user.user)
#         # shipping_address = ShippingAddress.objects.get(user=request.user)
#         # serializer2 = ShippingAddressSerializer(shipping_address).data
#         serializer = OrderItemSerializer(order_items, many=True)
#         if shipping_address is None:
#             serializer2 = "No Shipping address provided"
#         resp = {
#             'name': request.user.get_full_name(),
#             'shipping_address': serializer2,
#             'phone number': str(request.user.phone),
#             'pick_up_type': request.user.user.pick_up_type,
#             'order': serializer.data

#         }
#         return Response(resp, status=HTTP_200_OK)


# class ProcessOrderView(APIView):
#     def post(self, request, *args, **kwargs):
#         permission_classes = [IsUser]
#         transaction_id = datetime.datetime.now().timestamp()
#         data = request.data
#         print("data:", data['shipping_address']['address'])
#         try:
#             order, created = Orders.objects.update_or_create(
#                 user=request.user,
#                 paid=True,
#                 cart=False,
#             )
#             order.invoice_id = transaction_id
#             order.save()
#             shipping_address, created = ShippingAddress.objects.update_or_create(
#                 user=request.user,
#                 order=order,
#                 address=data['shipping_address']['address'],
#                 city=data['shipping_address']['city'],
#                 state=data['shipping_address']['state'],
#             )
#             shipping_address.save()
#             return Response({'message': 'Sucessful'}, status=HTTP_200_OK)
#         except:
#             return Response({'message': 'Order Could not be Processed'}, status=HTTP_400_BAD_REQUEST)
