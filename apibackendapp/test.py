from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from .models import  Employee,Department
from datetime import  date
from .serializers import EmployeeSerializer

class EmployeeViewSetTest(APITestCase):
    def setUp(self):
        self.department = Department.objects.create(DepartmentName="HR")
        self.employee = Employee.objects.create(
          EmployeeName="Jone Doe",
          Designation="Manager",
          DateOfJoining=date(2020,1,15),
          DepartmentId =self.department,
          contact="123456789",
          IsActive=True

        )

        self.client=APIClient()

    def test_employee_list(self):



         url=reverse('employee-list')
         response= self.client.get(url)
         

         employees = Employee.objects.all()
         serializer=EmployeeSerializer(employees,many=True)

         self.assertEqual(response.status_code,status.HTTP_200_OK)
    
         self.assertEqual(response.data,serializer.data)

    def test_employee_detail(self):



         url=reverse('employee-detail',args=[self.employee.EmployeeId])
         response= self.client.get(url)
         

         employees = Employee.objects.all()
         serializer=EmployeeSerializer(self.employee)

         self.assertEqual(response.status_code,status.HTTP_200_OK)
    
         self.assertEqual(response.data,serializer.data)
    
    def test_employee_create(self):

        url=reverse('employee-list')
        data={
              "EmployeeName":"Jonny Doe",
              "Designation":"Assistant",
              "DateOfJoining":"2025-06-24",
              "DepartmentId" :self.department.DepartmentId,
              "contact":"123456799",
              "IsActive":True
        }
        response= self.client.post(url, data , format='json')
         

        employees = Employee.objects.all()
        serializer=EmployeeSerializer(self.employee)

        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
        self.assertEqual(Employee.objects.count(),2)
        self.assertEqual(Employee.objects.get(EmployeeName="Jonny Doe").Designation,"Assistant")


    def test_employee_update(self):

        url=reverse('employee-detail',args=[self.employee.EmployeeId])
        data={
              "EmployeeName":"Jonny Dep",
              "Designation":"CEO",
              "DateOfJoining":"2025-06-24",
              "DepartmentId" :self.department.DepartmentId,
              "contact":"123456797",
              "IsActive":True
        }
        response= self.client.put(url, data , format='json')
         

        employees = Employee.objects.all()
        serializer=EmployeeSerializer(self.employee)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.employee.refresh_from_db()
        self.assertEqual(Employee.objects.get(EmployeeName="Jonny Dep").Designation,"CEO")


    def test_employee_search(self):
        url = reverse('employee-list')+'?search=Manager'
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertGreater(len(response.data),0)
        for employee in response.data:
            self.assertIn("Manager",employee['Designation'])



           

    def test_employee_delete(self):
        url = reverse('employee-detail',args=[self.employee.EmployeeId])
        response = self.client.delete(url)

        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
        self.assertEqual(Employee.objects.count(),0)
