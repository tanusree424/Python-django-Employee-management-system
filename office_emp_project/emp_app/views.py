from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import HttpResponse
from django.db.models import Q
from .models import Employee,Department,Role
from django.core.paginator import Paginator
def index(request):
  return render(request,'index.html')
# Create your views here.
def addemp(request):
   dept=Department.objects.all()
   role=Role.objects.all()
   data= {
     "depts":dept,
     "roles":role
   }
   if request.method=="POST":
     fname = request.POST.get("fname")
     lname = request.POST.get("lname")
     depart = request.POST.get("dept")
     
     sala  = request.POST.get("salary")
     bonuss = request.POST.get("bonus")
     hire_date = request.POST.get("hire_date")
     phone_num=  request.POST.get("phone_number")
     role_emp  = request.POST.get("role")
     emp_img = request.FILES.get('emp_img')
     department = Department.objects.get(id=depart)
     role_id = Role.objects.get(id=role_emp)
     employee=Employee(first_name=fname,last_name=lname,dept=department,salary=sala,bonus=bonuss,hire_date=hire_date,phone=phone_num,role=role_id,photo=emp_img)
     
     employee.save()
     messages.success(request,"Data Save Successfully")
     return redirect('all_emp')
     
   return render(request,"add-emp.html",data)
def showemp(request):
  employee= Employee.objects.all()
  paginator = Paginator(employee,3)
  page_number = request.GET.get("page") 
  employee_finalData = paginator.get_page(page_number)
  
  total_page = employee_finalData.paginator.num_pages
  if request.method=="GET":
    search_data = request.GET.get('search_term')
    data={}
    if search_data:
      employee_finalData = Employee.objects.filter(
        Q(first_name__icontains=search_data) |
        Q(last_name__icontains=search_data) 
        
      )
  
  data ={
    "employee_finalData": employee_finalData,
    "totalPagelist": [n+1 for n in range(total_page)]
  }
  return render(request,"show-emp.html",data)
def removeemp(request,emp_id=0):
  if emp_id:
    try:
      empId_to_be_removed = Employee.objects.get(id=emp_id)
      empId_to_be_removed.delete()
      return HttpResponse("Employee Deleted Successfully")
    except:
      return HttpResponse("Please Enter a valid employee id") 
  employee= Employee.objects.all()
  return render(request,'remove-emp.html',{"emps":employee})

  
def filteremp(request):
  if request.method == "POST":
    name = request.POST.get("name")
    depart = request.POST.get("dept")
    roles = request.POST.get("role")
    employee_finalData = Employee.objects.all()
    if name:
      employee_finalData=employee_finalData.filter(Q(first_name__icontains=name) | Q(last_name__icontains=name) ) 
      
    if depart:
      employee_finalData = employee_finalData.filter(dept__name=depart)
    if roles:
      employee_finalData = employee_finalData.filter(role__name=roles)
    data = {"employee_finalData":employee_finalData}
    return render(request,"show-emp.html",data)
  elif request.method =="GET":
    return render(request,"filter-emp.html")  
  else:
    return HttpResponse("Invalid occured No Record found")
  
  