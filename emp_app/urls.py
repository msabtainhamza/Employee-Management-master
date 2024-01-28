
from django.urls import path, include
from . import views

urlpatterns = [    
    path('', views.index, name='index'),
    path('all', views.all, name='all'),
    path('employeedata/<int:id>', views.employeedata, name='employeedata'),
    path('add', views.add, name='add'),
    path('remove/<int:emp_id>', views.remove, name='remove'),
    path('login', views.login, name='login'),
    path('login_process', views.login_process, name='login_process'),
    path('logout', views.logout, name='logout'),
    path('signup', views.signup, name='signup'),
    path('employee-portal/<int:id>', views.employee_portal, name='employee_portal'),
    path('applyforleave/<int:id>', views.applyforleave, name='applyforleave'),
    path('leaveaccepted/<int:id>', views.leaveaccepted, name='leaveaccepted'),
    path('leavedeclined/<int:id>', views.leavedeclined, name='leavedeclined'),
    path('leaveRejected/<int:id>', views.leaveRejected, name='leaveRejected'),
    path('markattendance/<int:id>', views.markattendance, name='markattendance'),
    path('addSalary/<int:id>', views.addSalary, name='addSalary'),
]
