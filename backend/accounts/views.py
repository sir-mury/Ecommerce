from functools import partial
from .models import CustomerProfile,BusinessProfile,User
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import CustomerProfileSerializer,BusinessProfileSerializer
from rest_framework import permissions, status
from rest_framework.response import Response
from dj_rest_auth.registration.views import RegisterView
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

class CustomRegisterView(RegisterView):
    queryset = User.objects.all()
    
class ProfileView(APIView):
    def get(self,request,*args,**kwargs):
        data = request.data
        if request.user.type == request.user.Types.CUSTOMER:
            customer = CustomerProfile.objects.get(user=request.user)
            serializer = CustomerProfileSerializer(customer)
            #serializer.is_valid()
            #print(serializer)
            return Response(data=serializer.data,status=status.HTTP_200_OK)
        elif request.user.type == request.user.Types.BUSINESS:
            business = BusinessProfile.objects.get(user=request.user)
            serializer = BusinessProfileSerializer(data,many=True)
            #serializer.is_valid()
            return Response(data=serializer.data,status=status.HTTP_200_OK)

    def post(self,request,*args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        data = request.data
        if request.user.type == request.user.Types.CUSTOMER:
            serializer = CustomerProfileSerializer(data=data) 
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        elif request.user.type == request.user.Types.BUSINESS:
            serializer = BusinessProfileSerializer(data=data)
            serializer.is_valid()
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)

    def patch(self,request,pk,*args, **kwargs):
        permission_classes = [permissions.IsAuthenticated]
        data = request.data
        if request.user.type == request.user.Types.CUSTOMER:
            profile = CustomerProfile.objects.get(user_id=pk)
            serializer = CustomerProfileSerializer(profile,data=data,partial=True) 
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response('Bad Request for customer',status=status.HTTP_400_BAD_REQUEST)
        elif request.user.type == request.user.Types.BUSINESS:
            profile = BusinessProfile.objects.get(user_id=pk)
            serializer = BusinessProfileSerializer(profile,data=data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
            return Response('Bad Request for business',status=status.HTTP_400_BAD_REQUEST)