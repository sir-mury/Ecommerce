from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import ShippingAddress, CustomerProfile, BusinessProfile
from allauth.account.utils import setup_user_email
from dj_rest_auth.registration.serializers import get_adapter


class ShippingAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShippingAddress
        fields = (
            'address', 'city', 'state'
        )

class BusinessProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = BusinessProfile
        fields = (
            'user', 'name', 'logo', 'cac', 'phone', 'address', 'rating', 'opening_time', 'closing_time'
        )


class CustomerProfileSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField('get_user_email')

    shipping_address = serializers.SerializerMethodField('get_shipping_address')

    class Meta:
        model = CustomerProfile
        fields = (
            'user', 'phone', 'first_name', 'last_name', 'date_of_birth', 'gender','shipping_address'
        )

    def get_shipping_address(self,request):
        customer = CustomerProfile.objects.get(user=request.user)
        address = ShippingAddressSerializer(customer.shippingaddress)
        return address.data

    def get_user_email(self, CustomerProfile):
        user = CustomerProfile.user.get_full_name()
        return user


class CustomRegisterSerializer(RegisterSerializer):
    type_choices = (
        ('CUSTOMER','Customer'),
        ('BUSINESS','Business'),
    )
    type = serializers.ChoiceField(choices=type_choices,allow_blank=False)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer,self).get_cleaned_data()
        print('type:',type)
        return {'username': self.validated_data.get('username', ''),
             'password1': self.validated_data.get('password1', ''),
             'email': self.validated_data.get('email', ''),
             'type': self.validated_data.get('type', '')
             }

    def save(self, request):
        adapter = get_adapter()
        user = adapter.new_user(request)
        self.cleaned_data = self.get_cleaned_data()
        user.type = self.cleaned_data.get('type')
        adapter.save_user(request, user, self)
        #self.custom_signup(request, user)
        setup_user_email(request, user, [])

        #user.type = self.cleaned_data.get('type')
        #user.save()
        return user
