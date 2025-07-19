from rest_framework import serializers
from .models import Employee,Department,User,UserDetails
from django.contrib.auth.models import User,Group
from django.contrib.auth.hashers import make_password
from  datetime import date


def date_of_joining_restriction(dateOfJoining):
    today=date.today()
    if dateOfJoining!=today:
        raise serializers.ValidationError("The Date of joining must be today")
        return dateOfJoining

def name_validation(employeeName):
    if len(employeeName)<3:
        raise serializers.ValidationError("Name must be atleast 3 letters and contain only alphabetic characters")
        return employeeName
class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Department
        fields='__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    Department=DepartmentSerializer(source='DepartmentId',read_only=True)

    DateOfJoining=serializers.DateField(validators=[date_of_joining_restriction])
    EmployeeName=serializers.CharField(max_length=200,validators=[name_validation])
    #nested serializer to include  Department details
    class Meta:
        model=Employee
        fields=('EmployeeId','EmployeeName','Designation','DateOfJoining','contact','IsActive','DepartmentId','Department')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=('id','username')

class UserDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model=UserDetails
        fields='__all__'

class SignupSerializer(serializers.ModelSerializer):
    group_name=serializers.CharField(write_only=True,required=False)

    def create(self,validated_data):
        group_name=validated_data.pop("group_name",None)
        validated_data["password"]=make_password(validated_data.get("password"))

        user=super(SignupSerializer,self).create(validated_data)

        if group_name:
            group,created=Group.objects.get_or_create(name=group_name)
            user.groups.add(group)
        return user
    class Meta:
        model=User
        fields=['username','password','group_name']
    
class LoginSerializer(serializers.ModelSerializer):
    username=serializers.CharField()

    class Meta:
        model=User
        fields=['username','password']
    