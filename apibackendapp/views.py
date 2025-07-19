from django.shortcuts import render
from rest_framework import viewsets,permissions
from .models import Employee,Department,User,UserDetails
from .serializers import EmployeeSerializer,DepartmentSerializer,UserSerializer,UserDetailsSerializer,SignupSerializer,LoginSerializer
from rest_framework import filters
from django.contrib.auth.models import Group
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


# Create your views here.
class EmployeeViewSet(viewsets.ModelViewSet):
    queryset=Employee.objects.all()
    serializer_class=EmployeeSerializer
    filter_backends=[filters.SearchFilter]
    search_fields=['EmployeeName','Designation']
    permission_classes=[AllowAny]

class DepartmentViewSet(viewsets.ModelViewSet):
      queryset= Department.objects.all()
      serializer_class=DepartmentSerializer
      permission_classes=[AllowAny]

class  UserViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[AllowAny]

class UserDetailsViewSet(viewsets.ModelViewSet):
     queryset=UserDetails.objects.all()
     serializer_class=UserDetailsSerializer
     permission_classes=[AllowAny]

class SignupAPIView(APIView):
    permission_classes=[AllowAny]

    def post(self,request):
        serializer=SignupSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.save()
            token,created=Token.objects.get_or_create(user=user)
            return Response( {
                "user_id":user.id,
                "username":user.username,
                "token":token.key,
                "role":user.groups.all()[0].id if user.groups.exists() else None
            },status=status.HTTP_201_CREATED)
        else:
            res={'status':status.HTTP_400_BAD_REQUEST,'data':serializer.errors}
            return Response(res,status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes=[AllowAny]
    def post(self,request): 
         serializer=LoginSerializer(data=request.data)
         if serializer.is_valid():
            username=serializer.validated_data["username"]
            password=serializer.validated_data["password"]
            user=authenticate(request,username=username,password=password)
            if user is not None:
                token=Token.objects.get(user=user)
                response={
                    "status":status.HTTP_200_OK,
                    "message":"success",
                    "username":user.username,
                    "role":user.groups.all()[0].id if user.groups.exists() else None,
                    "data":{
                        "Token":token.key
                    }
                }
                return Response(response,status=status.HTTP_200_OK)
            else:
                response={
                    "status":status.HTTP_400_UNAUTHORIZED,
                    "message":" Invalid email or password "

                }
                return Response(response,status-status.HTTP_401_UNAUTHORIZED)
         response={
             "status":status.HTTP_400_BAD_REQUEST,
             "message":"bad request",
             "data":serializer.errors
         }
         return response(response,status=status.HTTP_400_BAD_REQUEST)                
                            