from re import template
from django.http import HttpRequest,HttpResponse
from django.shortcuts import render
from datetime import datetime

#Using models
from .models import Department,Role,Employee
from django.db.models import Q


# Create your views here.
def index(request):
    return render(request,'index.html')

def all_emp(request): 

    # DbTable.objects.all() to get all DbTable object entries                         
    emps = Employee.objects.all() 

    # Context is type dict & used to pass value to template
    context ={
        'emps':emps
    }


    return render(request,'all_emp.html',context)

def add_emp(request):
    # Request can be either POST (With data) or Get (Just a request) 
    
    if request.method == 'POST':
        #Fetching the data
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        salary = int(request.POST['salary'])
        bonus = int(request.POST['bonus'])
        phone = int(request.POST['phone'])
        dept = int(request.POST['dept'])
        role = int(request.POST['role'])

        # Storing the data => create object & object.save() method call
        new_emp = Employee(first_name= first_name, last_name=last_name, salary=salary, bonus=bonus, phone=phone, dept_id = dept, role_id = role, hire_date = datetime.now())
        new_emp.save()
        return HttpResponse('Employee added Successfully')

    elif request.method=='GET': # render the page
        return render(request, 'add_emp.html')

    else:
        return HttpResponse("An Exception Occured! Employee Has Not Been Added")


def remove_emp(request , emp_id = 0): # Show details of Employee to be removed in dropdown
                                      # we can remove an employee with its unique ID
    if emp_id:
        try:
            emp_to_be_removed = Employee.objects.get(id=emp_id)
            emp_to_be_removed.delete()
            return HttpResponse("Employee Removed Successfully")
        except:
            return HttpResponse("Please Enter A Valid EMP ID")
    
    emps = Employee.objects.all()
    context = {
        'emps': emps
    }
    return render(request,'remove_emp.html',context)

def filter_emp(request):

    if request.method == 'POST':
        name = request.POST['name']
        dept = request.POST['dept']
        role = request.POST['role']
        emps = Employee.objects.all()

        # Q is used for complex queries with "AND","OR" in sql query
        if name:
            emps = emps.filter(Q(first_name__icontains = name) | Q(last_name__icontains = name))
        if dept:
            emps = emps.filter(dept__name__icontains = dept)
        if role:
            emps = emps.filter(role__name__icontains = role)

        context = {
            'emps': emps
        }
        return render(request, 'all_emp.html', context)

    elif request.method == 'GET':
        return render(request, 'filter_emp.html')
    else:
        return HttpResponse('An Exception Occurred')











