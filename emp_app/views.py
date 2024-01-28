
from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from . models import Employee, UserProfile, Leave, Attendance, SalarySlip
from .decoraters import unauthenticated_user, allowed_users
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def all(request):
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request, 'view.html', context)


def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def add(request):
    if request.method== "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        useremail = request.POST['email']
        dept = request.POST['dept']
        role = request.POST['role']

        # check if email already exists
        allemails = Employee.objects.all()
        emails = []
        for email in allemails:
            emails.append(email.email)
        if request.POST['email'] in emails:
            return HttpResponse("Email already exists! Please try again.")
        else:
            new_emp = Employee(first_name=first_name,last_name=last_name,salary=salary,bonus=bonus,dept=dept,role=role,phone=phone,hire_date = datetime.now(), email=useremail)
            new_emp.save()
            return render(request, "index.html")
    elif request.method == "GET":
        allemails = User.objects.all()
        emails = []
        for email in allemails:
            emails.append(email.email)

        context = {
            'emails': emails
        }
        return render(request, "add.html", context)
    else:
        return HttpResponse("An exception occured! Employee has not been added!")


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def remove(request, emp_id = 0):
    if emp_id:
        try:
            emp_delete = Employee.objects.get(id = emp_id)
            emp_delete.delete()
            return render(request, 'index.html')
        except:
            return HttpResponse("Oops! Something gone wrong.")
    emps = Employee.objects.all()
    context = {
        'emps' : emps
    }
    return render(request, 'remove.html', context)


@unauthenticated_user
def login(request):
    return redirect('login_process')


def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        group = Group.objects.get(name='employee')
        user.groups.add(group)
        UserProfile.objects.create(user=user, is_employee=True)
        messages.success(request, "Your account has been created successfully!")
        return redirect('login')
    else:
        messages.success(request, "An exception occured! Please try again.")

    return redirect('login')

@unauthenticated_user
def login_process(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        allUser = User.objects.all()

        allUserlogin = {}
        for user in allUser:
            allUserlogin[user.email] = user.username

        if username in allUserlogin.keys():
            user = authenticate(username=allUserlogin[username], password=password)
            if user is not None:
                auth_login(request, user)
                # find email of user
                user = User.objects.get(username=allUserlogin[username])
                if user.groups.filter(name='employee').exists():
                    emp = Employee.objects.get(email=user.email)
                    return redirect('employee_portal', id=emp.id)
                else:
                   return redirect('index')
            else:
                return HttpResponse("Invalid password! Please try again.")
        else:
            return HttpResponse("Invalid credentials! Please try again.")
    else:
        messages.success(request, "An exception occured! Please try again.")
    
    return render(request, 'login.html')


@allowed_users(allowed_roles=['employee'])
@login_required(login_url='login')
def employee_portal(request, id):
    emp = Employee.objects.get(id = id)

    # check for today's attendance
    today = datetime.now().date()
    attendances = Attendance.objects.all()
    attendance = []
    
    for att in attendances:
        if att.date == today and att.emp.id == id:
            attendance.append(att)

        # get all salaries of employee of this id
    salaries = SalarySlip.objects.all()

    empsalaries = []
    for salary in salaries:
        if salary.emp.id == id:
            empsalaries.append(salary)


    context = {
        'first_name': emp.first_name,
        'last_name': emp.last_name,
        'salary': emp.salary,
        'bonus': emp.bonus,
        'dept': emp.dept,
        'role': emp.role,
        'phone': emp.phone,
        'hire_date': emp.hire_date,
        'email': emp.email,
        'status': emp.status,
        'attendance': attendance,
        'attendance_len': len(attendance),
        'id': id,
        'salaries': empsalaries,
        'salaries_len': len(empsalaries),
    }
    return render(request, 'Employee_Portal.html', context)


@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def employeedata(request, id):
    emp = Employee.objects.get(id = id)
    
    # get all leaves of employee of this id
    leaves = Leave.objects.all()

    
    emp_leaves = []
    for leave in leaves:
        if leave.emp.id == id:
            emp_leaves.append(leave)

    attendances = Attendance.objects.all()

    emp_attendances = []
    for attendance in attendances:
        if attendance.emp.id == id:
            emp_attendances.append(attendance)


    context = {
        'id' : id,
        'first_name': emp.first_name,
        'last_name': emp.last_name,
        'salary': emp.salary,
        'bonus': emp.bonus,
        'dept': emp.dept,
        'role': emp.role,
        'phone': emp.phone,
        'hire_date': emp.hire_date,
        'email': emp.email,
        'status': emp.status,
        'emp_leaves': emp_leaves,
        'emp_leves_len': len(emp_leaves),
        'emp_attendances': emp_attendances,
    }
    return render(request, 'employeedata.html', context)

@allowed_users(allowed_roles=['employee'])
@login_required(login_url='login')
def applyforleave(request, id):
    if request.method == "POST":
        emp = Employee.objects.get(id = id)
        start_date = request.POST.get('date')
        number_of_days = int(request.POST.get('days'))
        arr = start_date.split('-')
        end_date = int(arr[2]) + number_of_days
        # make acorrding to 31 days and 30 days
        if end_date > 31:
            end_date = end_date - 31
            if int(arr[1]) == 12:
                arr[1] = 1
                arr[0] = int(arr[0]) + 1
            else:
                arr[1] = int(arr[1]) + 1
        else:
            end_date = end_date

        end_date = str(arr[0]) + '-' + str(arr[1]) + '-' + str(end_date)

        reason = request.POST.get('reason')
        new_leave = Leave(emp=emp, start_date=start_date, end_date=end_date, reason=reason)
        new_leave.save()

        return redirect('employee_portal', id=id)
    else:
        return HttpResponse("An exception occured! Please try again.")
    

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def leaveaccepted(request, id):
    if request.method == "POST":
        leave = Leave.objects.get(id=id)
        leave.emp.status = "Leave"
        leave.emp.save()
        emp_id = leave.emp.id
        leave.status = "Approved"
        leave.save()
        return redirect('employeedata', id=emp_id)
    else:
        return HttpResponse("An exception occured! Please try again.")
    

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def leavedeclined(request, id):
    if request.method == "POST":
        leave = Leave.objects.get(id=id)
        leave.emp.status = "Active"
        leave.emp.save()
        emp_id = leave.emp.id
        leave.status = "Pending"
        leave.save()
        return redirect('employeedata', id=emp_id)
    else:
        return HttpResponse("An exception occured! Please try again.")
    

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def leaveRejected(request, id):
    if request.method == "POST":
        leave = Leave.objects.get(id=id)
        leave.emp.status = "Active"
        leave.emp.save()
        emp_id = leave.emp.id
        leave.status = "Rejected"
        leave.save()
        return redirect('employeedata', id=emp_id)
    else:
        return HttpResponse("An exception occured! Please try again.")

@allowed_users(allowed_roles=['employee'])
@login_required(login_url='login')
def markattendance(request, id):
    if request.method == "POST":
        emp = Employee.objects.get(id = id)
        date = datetime.now().date()
        time = datetime.now().time()
        new_attendance = Attendance(emp=emp, date=date, time=time, status="Present")
        new_attendance.save()
        return redirect('employee_portal', id=id)
    else:
        return HttpResponse("An exception occured! Please try again.")
    

@allowed_users(allowed_roles=['admin'])
@login_required(login_url='login')
def addSalary(request, id):
    if request.method == "POST":
        emp = Employee.objects.get(id = id)
        month = request.POST.get('month')
        salary = int(request.POST.get('salary'))
        bonus = int(request.POST.get('bonus'))

        new_salary = SalarySlip(emp=emp, month=month, salary=salary, bonus=bonus)
        new_salary.save()
        return redirect('employeedata', id=id)
    else:
        return HttpResponse("An exception occured! Please try again.")

