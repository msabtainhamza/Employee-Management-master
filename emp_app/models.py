from django.db import models
from django.contrib.auth.models import User


class Employee(models.Model):
    first_name = models.CharField(max_length=100,null=False)
    last_name = models.CharField(max_length=100)
    dept = models.CharField(max_length=100)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    role = models.CharField(max_length=100)
    phone = models.IntegerField(default=0)
    email = models.EmailField(max_length=100, default="")
    hire_date = models.DateField()
    status = models.CharField(max_length=100, choices=(('Active', 'Active'), ('Leave', 'Leave')), default='Active')

    def __str__(self):
        return "%s %s " %(self.first_name, self.last_name)

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    is_employee = models.BooleanField(default=True)  # True for employees, False for admins

    def __str__(self):
        return self.user.username

class Leave(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=(('Approved', 'Approved'), ('Pending', 'Pending'), ('Rejected', 'Rejected')), default='Pending')

    def __str__(self):
        return "%s %s " %(self.emp.first_name, self.emp.last_name)
    
class Attendance(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    status = models.CharField(max_length=100, choices=(('Present', 'Present'), ('Absent', 'Absent')), default='Absent')

    def __str__(self):
        return "%s %s " %(self.emp.first_name, self.emp.last_name)
    
    
class SalarySlip(models.Model):
    emp = models.ForeignKey(Employee, on_delete=models.CASCADE)
    month = models.CharField(max_length=100)
    salary = models.IntegerField(default=0)
    bonus = models.IntegerField(default=0)
    
    def __str__(self):
        return "%s %s " %(self.emp.first_name, self.emp.last_name)
    
