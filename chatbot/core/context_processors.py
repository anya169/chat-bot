from core.models import Special_Question, Employee
from django.utils import timezone
from datetime import timedelta


def sidebar_notifications(request):
   return {
      'unanswered_count': Special_Question.objects.filter(answer__isnull=True).count()
   }
  
def sidebar_new_employee(request):
   employee_name = Employee.objects.order_by('-telegram_registration_date').first().name if Employee.objects.exists() else None
   employee_date = Employee.objects.order_by('-telegram_registration_date').first().telegram_registration_date if Employee.objects.exists() else None
   return {
      'new_employee_name': employee_name,
      'new_employee_date': employee_date
   }
   
   
def sidebar_new_employees_in_week(request):

   week_ago = timezone.now() - timedelta(days=7)
   
   employees = Employee.objects.filter(telegram_registration_date__gte=week_ago).order_by('-telegram_registration_date') if Employee.objects.exists() else None

   data = []
   for emp in employees:
      data.append({
         'new_employee_name': emp.name,
         'new_employee_date': emp.telegram_registration_date
      })
      
   return {
      'week_data': data
   }