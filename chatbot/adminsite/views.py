from django.shortcuts import render
from .models import *


def young_employee_list(request):
   employees = Employee.objects.filter(is_curator=False, is_admin=False)
   return render(request, 'employees/list.html', {'employees': employees})


