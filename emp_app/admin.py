from django.contrib import admin
from .models import Employee, UserProfile, Leave, Attendance, SalarySlip

# Register your models here.
admin.site.register(Employee)
admin.site.register(UserProfile)
admin.site.register(Leave)
admin.site.register(Attendance)
admin.site.register(SalarySlip)
