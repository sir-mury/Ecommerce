from django.db.models.query_utils import DeferredAttribute
from products.models import Product
from accounts.models import User
from django.conf import settings
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save


# Create your models here.
class Orders(models.Model):
    delivery_choices = (
        ('Door Delivery', 'Door Delivery'),
        ('Pickup Station', 'Pickup Station'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,db_constraint=False, on_delete=models.CASCADE, related_name='user_order')
    # business
    pick_up_type = models.CharField(
        max_length=20, choices=delivery_choices, default='Door Delivery')
    is_delivery = models.BooleanField(default=True)
    paid = models.BooleanField(default=False)
    #cart = models.BooleanField(default=True)
    # delivery
    invoice_id = models.CharField(max_length=255, blank=True, null=True)
    date_created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ('-date_created',)
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return str(self.id)

    @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    def create_order(sender, instance, created, **kwargs):
        #print('hello:',instance.type)
        if created and instance.type == sender.Types.CUSTOMER:
            #print('order created')
            Orders.objects.create(user=instance)
        elif created and instance.type == sender.Types.BUSINESS:
            print('order not created')
            pass
        else:
            #print('order updated')
            instance.user_order.update()

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def save_order(sender, instance, **kwargs):
    #     print('Problem is from saving order')
    #     instance.user.save()

    @property
    def get_order_total(self):
        orderItems = self.orderitems.all()
        total = sum([items.get_total for items in orderItems])
        return total

    @property
    def get_order_items(self):
        orderItems = self.orderitems.all()
        total = sum([items.quantity for items in orderItems])
        return total


class OrderItem(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, blank=True, null=True)
    orders = models.ForeignKey(Orders, on_delete=models.SET_NULL,
                              blank=True, null=True, related_name='orderitems')
    quantity = models.IntegerField(default=1, blank=True, null=True)

    class Meta:
        verbose_name = 'Order Item'
        verbose_name_plural = 'Order Items'

    def __str__(self):
        return self.product.name

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
