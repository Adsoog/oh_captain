from django.shortcuts import render
from apps.rrhh.models.employee_models import Employee

def employees_list(request):
    employees = Employee.objects.all()
    context = {
        'employees': employees,
    }
    return render(request, 'rrhh/employees/employees_list.html', context)