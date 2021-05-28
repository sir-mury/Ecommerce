from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Business, Customer, User,BusinessProfile,CustomerProfile,ShippingAddress #Business, Customer,  ShippingAddress
# Register your models here.


class MyUserAdmin(UserAdmin):
    list_display = ['email','type','date_created', 'is_active', 'is_staff']
    search_fields = ['email','type']
    readonly_fields = ['date_created', 'last_login']
    filter_horizontal = []
    # fieldsets = (
    #     (None, {'fields': ('email', 'password')}),
    #     ('Permissions', {'fields': ('is_staff', 'is_active')}),
    # )
    fieldsets = []
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'type','password1', 'password2', 'is_staff', 'is_active')}
         ),
    )
    list_filter = ['type']
    ordering = ['email', 'password',]


admin.site.register(User, MyUserAdmin)
# admin.site.register(Customer)
# admin.site.register(Business)

@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ['customer_email', 'address', 'state']
    list_filter = ['address']
    search_fields = ['address']
    #fields = ['customer_email','address','state']

    def customer_email(self,obj):
        return obj.customer.user.email

@admin.register(CustomerProfile)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'gender']
    list_filter = ['user']
    search_fields = ['user']

@admin.register(BusinessProfile)
class BusinessAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'verified']
    list_filter = ['user','name']
    search_fields = ['user','name']
