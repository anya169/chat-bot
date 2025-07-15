from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages


#авторизация
def login_user(request):
   
   if request.method == 'POST':
      username = request.POST.get("username")
      password = request.POST.get("password")
      
      user = authenticate(request, username=username, password=password)
         
      if user is not None:
         login(request, user)
         try:
            # Получаем профиль сотрудника
            employee = Employee.objects.get(login=username)
            
            # Перенаправляем по ролям
            if employee.is_admin:
               return redirect('admin_account')
            elif employee.is_curator:
               return redirect('curator_account')
            else:
               messages.error(request, 'Недостаточно прав для доступа')
               return redirect('login_page')  
            
         except Employee.DoesNotExist:
               messages.error(request, 'Профиль сотрудника не найден')
               return redirect('login_page')
      else:
         messages.error(request, 'Неверный логин или пароль')
         return redirect('login_page')  

   return render(request, 'personal_account/login.html')


#вход
def login_page(request):
   return render(request, 'personal_account/login.html')

#личный кабинет администратора
def admin_account(request):
   return render(request, 'admin_account.html')

#личный кабинет куратора
def curator_account(request):
   return render(request, 'curator_account.html')

#получение списка молодых сотрудников
def young_employee_list(request):
   employees = Employee.objects.filter(is_curator=False, is_admin=False)
   return render(request, 'employees/list.html', {'employees': employees})


   
