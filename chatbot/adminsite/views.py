from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth import logout
from chatbot import settings
from .models import *
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
import os
from django.http import FileResponse, JsonResponse
from django.contrib.auth.decorators import login_required
import json
from datetime import datetime
from django.core.paginator import Paginator
from django.utils import timezone
from django.db.models import Count

#авторизация
@csrf_exempt
def login_user(request):
   if request.user.is_authenticated:
      return redirect('curator_account')
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
            if employee.is_curator:
               request.session['user_login'] = employee.login
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

#выход пользователя
@csrf_exempt
def logout_view(request):
   logout(request)
   #очищаем сессию
   request.session.flush()
   return redirect(f'{settings.LOGIN_URL}?logout=true')

@login_required
#личный кабинет куратора
def curator_account(request):
   cur_login = request.session.get('user_login')
   employee = Employee.objects.filter(login = cur_login).first
   count = Employee.objects.filter(curator_login = cur_login).count()
   return render(request, 'personal_account/curator_account.html', {'employee': employee, 'count': count})

@login_required
#чаты куратора
def chats(request):
   #извлекаем из сессии текущего куратора
   cur_login = request.session.get('user_login')
   
   #получаем всех его сотрудников
   employees = Employee.objects.filter(curator_login = cur_login)
   #получаем айди всех его сотрудников
   employees_ids = []
   for employee in employees:
      employees_ids.append(employee.id)
   #делаем выборку айди сотрудников
   employees_ids_with_questions = (
      Special_Question.objects
      .filter(employee_id__in=employees_ids)  # только подопечные текущего куратора
      .values_list('employee_id', flat=True)  # берём только ID сотрудников
      .distinct()  # убираем дубликаты
   )

   #считаем неотвеченные вопросы
   unanswered_counts = (
      Special_Question.objects
      .filter(employee_id__in=employees_ids, answer__isnull=True)
      .values('employee_id')
      .annotate(count=Count('id'))
   )
   unanswered_dict = {item['employee_id']: item['count'] for item in unanswered_counts}

   #получаем сотрудников с вопросами и добавляем информацию о неотвеченных
   employees_with_questions = []
   for employee in Employee.objects.filter(id__in=employees_ids_with_questions):
      employee.unanswered_count = unanswered_dict.get(employee.id, 0)
      employees_with_questions.append(employee)

   return render(request, 'chats/chats.html', {'employees_with_questions': employees_with_questions})

@login_required
#чат с сотрудником
def chat_with_employee(request, employee_id):
   employee = Employee.objects.filter(id=employee_id).first()
   questions_answers = Special_Question.objects.filter(
      employee_id=employee
   ).order_by('-creation_question')
   
   return render(request, 'chats/detailed_chat.html', {
      'employee': employee,
      'questions_answers': questions_answers
   })

def answer_question(request, question_id):
   if request.method == 'POST':
      question = Special_Question.objects.get(id=question_id)
      question.answer = request.POST.get('answer')
      question.creation_answer = timezone.now()
      question.save()
      return JsonResponse({'success': True})
   return JsonResponse({'success': False}, status=400)

@login_required
#страница для формирования отчета  
def report_page(request): 
   #передаем всех сотрудников
   employees = Employee.objects.filter(is_curator = False).order_by('-hire_date')  
   filials = Filial.objects.all()
   structs = Struct.objects.all()
   numtabs = employees.values_list('num_tab', flat=True)
   curators = Employee.objects.filter(is_curator = True)
   polls = Poll.objects.exclude(name='Опрос через 14 дней')
   data = []
   for emp in employees:
      if (emp.curator_login):
         curator = Employee.objects.filter(login=emp.curator_login).first()
      else:
         curator = None
      data.append({
               'id': emp.id,
               'name': emp.name,
               'filial': emp.filial.name if emp.filial else None,
               'struct': emp.struct.name if emp.struct else None,
               'num_tab': emp.num_tab,
               'hire_date': emp.hire_date.strftime('%d.%m.%Y') if emp.hire_date else None,
               'telegram_registration_date': emp.telegram_registration_date.strftime('%d.%m.%Y') if emp.telegram_registration_date else None,
               'curator_login': emp.curator_login,
               'curator': f"{curator.name}" if curator else None
            })
   paginator = Paginator(data, 50)  #по 50 строк на странице
   page_number = request.GET.get('page', 1)
   page_obj = paginator.get_page(page_number)
   #получаем все существующие рассылки
   mailings = Mailing.objects.all()
   return render(request, 'employees/generate_report.html', 
                 {'employees': page_obj.object_list, 
                  'filials': filials, 
                  'structs': structs, 
                  'numtabs': numtabs,
                  'curators': curators, 
                  'polls': polls, 
                  'mailings': mailings,
                  'current_user': request.user.username,
                  'page_obj': page_obj,
                  'page_range': paginator.get_elided_page_range(page_obj.number)
               })

@login_required
def download_report(request):
   try:
      #генерируем отчет 
      data = json.loads(request.body)
      emp_ids = [str(emp['id']) for emp in data['employees']]
      poll_names = data['polls']
      #импортируем функцию
      from .generate_report import generate_report
      report_filename = generate_report(request.user.username, emp_ids, poll_names)
      
      if not report_filename or not os.path.exists(report_filename):
         from django.http import HttpResponse
         return HttpResponse("Ошибка: файл отчета не найден", status=500)
      
      #открываем файл в бинарном режиме
      file = open(report_filename, 'rb')
      response = FileResponse(file)
      response['Content-Disposition'] = f'attachment; filename="{os.path.basename(report_filename)}"'

      return response
      
   except Exception as e:
      return HttpResponse(f"Ошибка: {str(e)}", status=500)

@login_required      
#информация о сотруднике
def employee(request, employee_id):
   employee = Employee.objects.filter(id=employee_id).first()
   #все его пройденные опросы
   polls = Poll.objects.filter(question__answer__login = employee.id).distinct()
  
   polls_data = []
   for poll in polls:
      questions_answers = []
      poll_questions = Question.objects.filter(poll_id=poll.id)
      for poll_question in poll_questions:
         poll_answer = Answer.objects.filter(question_id=poll_question.id, login=employee).first()
         #cохраняем пару (вопрос, ответ)
         questions_answers.append({
            'question': poll_question,
            'answer': poll_answer
         })
      polls_data.append({
         'poll': poll,
         'questions_answers': questions_answers
      })
   count = polls.count()
   return render(request, 'personal_account/employee.html', {
      'employee': employee,
      'polls_data': polls_data,
      'count': count
   })   

@login_required   
#статистика
def statistic(request):
   employees = Employee.objects.filter(is_curator=False)
   filials = Filial.objects.all()
   #сотрудники, воспользовавшиеся ботом
   bot_employees = employees.filter(
      telegram_registration_date__isnull=False     
   )
   #не воспользовавшиеся
   not_bot_employees = employees.filter(telegram_registration_date__isnull=True)
   bot_chart_data = {
      'labels': ['Зарегистрированы в боте', 'Не зарегистрированы'],
      'data': [bot_employees.count(), not_bot_employees.count()],
      'colors': ['#0078C1', '#EEEEEE']
   }
   #люди, воспользовавшиеся ботом по филиалам
   bot_chart_filial_data = {
      'labels': [],
      'bot_users': [],
      'total_users': [],
      'percentages': []
   }
   for filial in filials:
         # Все сотрудники филиала
         all = employees.filter(filial=filial).count()
         if all == 0:
            continue
         # Сотрудники филиала с ботом
         bot_users = employees.filter(
            filial=filial,
            telegram_registration_date__isnull=False
         ).count()
         
         # Процент использования
         percentage = round((bot_users / all) * 100) if all > 0 else 0
         
         bot_chart_filial_data['labels'].append(filial.name)
         bot_chart_filial_data['bot_users'].append(bot_users)
         bot_chart_filial_data['total_users'].append(all)
         bot_chart_filial_data['percentages'].append(percentage)
         
  
   return render(request, 'statistic/statistic.html', {
      'employee': employees,
      'bot_chart_data': bot_chart_data,
      'bot_chart_filial_data': bot_chart_filial_data,
   })

#фильтрация
@csrf_exempt   
def filter_employees(request):
   cur_login = request.session.get('user_login')
   if request.method == 'POST':
      try:
         filters = json.loads(request.body)
         is_filter = False
         employees = Employee.objects.filter(is_curator = False) 
         
         if filters.get('all'):
            is_filter = True   
         else:
            if filters.get('name'):
               employees = employees.filter(name__in=filters['name'])   
               is_filter = True     
            if filters.get('filial'):
               employees = employees.filter(filial__in=filters['filial'])     
               is_filter = True       
            if filters.get('struct'):
               employees = employees.filter(struct__in=filters['struct'])
               is_filter = True 
            if filters.get('numtab'):
               employees = employees.filter(num_tab__in=filters['numtab'])
               is_filter = True 
            if filters.get('curator'):
               curator_logins = Employee.objects.filter(
                  is_curator=True,
                  name__in=filters['curator']
               ).values_list('login', flat=True)               
               employees = employees.filter(curator_login__in=curator_logins)
               is_filter = True   
            if filters.get('hire_date_from'):
               hire_from = datetime.strptime(filters['hire_date_from'], '%d.%m.%Y').date()
               employees = employees.filter(hire_date__gte=hire_from)          
               is_filter = True  
            if filters.get('hire_date_to'):
               hire_to = datetime.strptime(filters['hire_date_to'], '%d.%m.%Y').date()
               employees = employees.filter(hire_date__lte=hire_to)
               is_filter = True 
            if filters.get('tg_date_from'):
               tg_from = datetime.strptime(filters['tg_date_from'], '%d.%m.%Y').date()
               employees = employees.filter(telegram_registration_date__gte=tg_from)   
               is_filter = True        
            if filters.get('tg_date_to'):
               tg_to = datetime.strptime(filters['tg_date_to'], '%d.%m.%Y').date()
               employees = employees.filter(telegram_registration_date__lte=tg_to)
               is_filter = True 
            if filters.get('own'):
               employees = employees.filter(curator_login=cur_login)   
               is_filter = True 
         employees = employees.order_by('-hire_date')  
         paginator = Paginator(employees, 50)  #по 50 строк на странице
         page_number = filters.get('page', 1)
         page_obj = paginator.get_page(page_number)
         # Подготовка данных для ответа
         employees_data = []
         for emp in page_obj.object_list:
            if (emp.curator_login):
               curator = Employee.objects.filter(login=emp.curator_login).first()
            else:
               curator = None
            employees_data.append({
               'id': emp.id,
               'name': emp.name,
               'filial': emp.filial.name if emp.filial else None,
               'struct': emp.struct.name if emp.struct else None,
               'num_tab': emp.num_tab,
               'hire_date': emp.hire_date.strftime('%d.%m.%Y') if emp.hire_date else None,
               'telegram_registration_date': emp.telegram_registration_date.strftime('%d.%m.%Y') if emp.telegram_registration_date else None,
               'curator_login': emp.curator_login,
               'curator': f"{curator.name}" if curator else None,
            })
            
         return JsonResponse({
               'employees': employees_data,
               'is_filter': is_filter,
               'page_obj': {
                  'number': page_obj.number,
                  'has_previous': page_obj.has_previous(),
                  'previous_page_number': page_obj.previous_page_number() if page_obj.has_previous() else None,
                  'has_next': page_obj.has_next(),
                  'next_page_number': page_obj.next_page_number() if page_obj.has_next() else None,
                  'paginator': {
                     'num_pages': page_obj.paginator.num_pages
                  }
               },
               'page_range': list(range(1, paginator.num_pages + 1))    
         })
         
      except Exception as e:
         return JsonResponse({'Ошибка': str(e)}, status=400)
   
   return JsonResponse({'error': 'Ошибка запроса'}, status=400)   

@login_required
#рассылки
def mailings(request):
   #получаем все существующие рассылки
   mailings = Mailing.objects.all()

   return render(request, 'employees/mailings.html', {'mailings': mailings})

@login_required      
#информация о рассылке
def mailing(request, mailing_id):
   mailing = Mailing.objects.filter(id=mailing_id).first()
   #вложения рассылки
   attachments = MailingAttachment.objects.filter(mailing_id = mailing.id).distinct()
  
   return render(request, 'employees/mailing.html', {
      'mailing': mailing,
      'attachments': attachments,
   })   

#удаление рассылки
@csrf_exempt   
def delete_mailing(request):
   if request.method == 'POST':
      try:
         id = json.loads(request.body)
         #удаляем рассылку и ее вложения
         mailing = Mailing.objects.filter(id = id).delete()
         attachments = MailingAttachment.objects.filter(mailing_id = id).delete()
         
         return JsonResponse({
            'success': True,
            'message': 'Рассылка успешно удалена'
        })
         
      except Exception as e:
         return JsonResponse({'Ошибка': str(e)}, status=400)
   
   return JsonResponse({'error': 'Ошибка запроса'}, status=400)   

#информация о рассылке
@csrf_exempt
def get_mailings(request):
   mailings = Mailing.objects.all().values('id', 'tag', 'name', 'description')
   return JsonResponse(list(mailings), safe=False)


   
