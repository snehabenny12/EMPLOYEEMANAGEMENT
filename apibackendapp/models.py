from django.db import models
from django.contrib.auth.models import User,Group
# Create your models here.
class Department(models.Model):
    DepartmentId=models.AutoField(primary_key=True)
    DepartmentName=models.CharField(max_length=100)


#whenver you print an instance
    def __str__(self):
        return self.DepartmentName


class Employee(models.Model):
      EmployeeId=models.AutoField(primary_key=True)
      EmployeeName=models.CharField(max_length=100)
      Designation=models.CharField(max_length=100)
      DateOfJoining=models.DateField()
      DepartmentId=models.ForeignKey(Department,on_delete=models.CASCADE)
      contact=models.CharField(max_length=15)
      IsActive=models.BooleanField(default=True)

      def __str__(self):
         return self.EmployeeName

class UserDetails(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,related_name='user_details')
    phoneno=models.CharField(max_length=15)
    email=models.EmailField()

    def __str__(self):
        return self.user.username