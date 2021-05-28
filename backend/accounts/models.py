from enum import unique
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
)
from django.db.models.fields import related
from phone_field import PhoneField
from django.conf import settings
#from products.models import Orders,Products
from django.dispatch import receiver
from django.db.models.signals import post_save
#sfrom products.models import Product
# Create your models here.


class UserManager(BaseUserManager):
    def create_user(self,email,type,password=None):
        if not type:
            raise ValueError("User must have a type")
        if not email:
            raise ValueError("User must have either an email address")
        user = self.model(
            email=self.normalize_email(email),
            type=type
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,password,type=None):
        #print('type:',type)
        user = self.create_user(
            email=self.normalize_email(email),
            type=type,
            password=password,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    class Types(models.TextChoices):
        CUSTOMER = 'CUSTOMER','Customer'
        BUSINESS = 'BUSINESS', 'Business'
    #TYPES = (('CUSTOMER', 'Customer'), ('BUSINESS', 'Business'),)
    type = models.CharField(max_length=50,choices=Types.choices,default=Types.CUSTOMER)
    email = models.EmailField(unique=True, max_length=65)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


    def get_full_name(self):
        return self.email

    def get_short_name(self):
        return self.email

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

class CustomerManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.CUSTOMER)

class BusinessManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(type=User.Types.BUSINESS)

class Customer(User):
    base_type = User.Types.CUSTOMER
    objects = CustomerManager()
    class Meta:
        proxy = True
    @property
    def orders(self):
        return self.orders

    @property
    def profile(self):
        return self.customerprofile

    def save(self):
        if not self.pk:
            self.type = User.Types.CUSTOMER
        return super().save()

class Business(User):
    base_type = User.Types.BUSINESS
    objects = BusinessManager()
    class Meta:
        proxy = True

    @property
    def profile(self):
        return self.businessprofile

    @property
    def product(self):
        return self.product

    def save(self):
        if not self.pk:
            self.type = User.Types.BUSINESS
        return super().save()


class CustomerProfile(models.Model):
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'),)
    user = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)
    phone = PhoneField(max_length = 15,unique=True,null=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    gender = models.CharField(choices=GENDER_CHOICES,
                              max_length=15, default="male")
    date_of_birth = models.DateField(max_length=8, blank=True, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name
        

class BusinessProfile(models.Model):
    user = models.OneToOneField(Business,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=100,blank=False,null=False)
    phone = PhoneField(max_length = 15,unique=True,null=True)
    logo = models.ImageField(null=True,blank=True)
    address = models.CharField(max_length=255,blank=False,null=False)
    cac = models.CharField(max_length=70,blank=True,null=True)
    verified = models.BooleanField(default=False)
    # products = models.ManyToManyField(Products,blank=True)
    # sales = models.ManyToManyField(Products,blank=True)
    # returns = models.ManyToManyField(Products,blank=True)
    rating = models.FloatField(max_length=15)
    opening_time = models.TimeField()
    closing_time = models.TimeField()

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    customer = models.OneToOneField(
        CustomerProfile, on_delete=models.CASCADE,primary_key=True)
    # order = models.ForeignKey(
    #     Orders, on_delete=models.CASCADE, related_name='users_order')
    address = models.CharField(max_length=500, null=False)
    city = models.CharField(max_length=255, null=False)
    state = models.CharField(max_length=255, null=False)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address

    @receiver(post_save, sender=CustomerProfile)
    def create_shipping_address(sender, instance, created, **kwargs):
        if created:
            print('shipping address created')
            ShippingAddress.objects.create(customer=instance)
        else:
            print('shipping address updated')
            ShippingAddress.objects.update(customer=instance)
            # user = instance.user
            # user.users_address.update()
            # instance.users_orders.update()

    # @receiver(post_save, sender=settings.AUTH_USER_MODEL)
    # def save_shipping_address(sender, instance, **kwargs):
    #     instance.user.update()

    
