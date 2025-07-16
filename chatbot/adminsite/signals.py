from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *

#отслеживаем отправку вопроса от сотрудника куратору через изменения в бд
@receiver(post_save, sender=Special_Question)
def create_new_chat(sender, instance, created, **kwargs):
   #если был задан вопрос
   if created:
      employee_id = instance.employee_id
      #получаем имя сотрудника, задавшего вопрос
      employee = Employee.objects.get(id = employee_id)
      employee_name = employee.name
      #получаем логин куратора, которому он адресован
      curator_login = employee.curator_login
      
      notification = f"Сотрудник {employee_name} задал новый вопрос!"
      
      