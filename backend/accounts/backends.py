from .models import User
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import check_password

class PhoneBackend:

    def authenticate(self,request,username=None,password=None,**kwargs):
        try:
            user = User.objects.get(phone=username)
            if getattr(user,'is_active') and user.check_password(password):
                return user
        except User.DoesNotExist:
            return None
        
        
        return None

    def get_user(self , user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist :
            return None