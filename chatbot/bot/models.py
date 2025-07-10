from django.db import models

class Employee(models.Model):
   service_number = models.IntegerField(unique=True, primary_key=True, verbose_name="Табельный номер")
   name = models.CharField(max_length=30, verbose_name="Имя")
   surname = models.CharField(max_length=100, verbose_name="Фамилия")
   department = models.ForeignKey(
      'Department',
      on_delete=models.CASCADE
   )
   is_curator = models.BooleanField(verbose_name='Является ли куратором')
   is_admin = models.BooleanField(verbose_name='Является ли администратором')
   telegram_id = models.IntegerField(unique=True, verbose_name="Telegram ID")
   hire_date = models.DateField(verbose_name="Дата приёма на работу")
   telegram_registration_date = models.DateField(auto_now_add=True, verbose_name="Дата первого обращения к боту")

   class Meta:
      db_table = 'Employee'
      verbose_name = "Сотрудник"
      verbose_name_plural = "Сотрудники"


class Department(models.Model):
   department_id = models.IntegerField(unique=True, primary_key=True, verbose_name='ID отдела')
   department_name = models.CharField(max_length=100, unique=True, verbose_name="Название отдела")
  
   class Meta:
      db_table = 'Department'
      verbose_name = "Отдел"
      verbose_name_plural = "Отделы"
      
class Poll(models.Model):
   poll_id = models.IntegerField(primary_key=True, unique=True, verbose_name='ID опроса')
   poll_name = models.CharField(verbose_name='Название опроса')
   poll_description = models.CharField(verbose_name='Описание опроса')   
   poll_duration = models.DurationField(blank=True)
   is_unexpected = models.BooleanField(verbose_name='Является ли внеплановым')      

   class Meta:
      db_table = 'Poll'
      verbose_name = 'Опрос'
      verbose_name_plural = 'Опросы'


class Question(models.Model):
   question_id = models.IntegerField(primary_key=True, unique=True, verbose_name='ID вопроса')
   question_name = models.CharField(verbose_name='Название вопроса')
   poll = models.ForeignKey(
      'Poll',
      on_delete=models.CASCADE
   )

   class Meta:
      db_table = 'Question'
      verbose_name = 'Вопрос'
      verbose_name_plural = 'Вопросы'


class Answer(models.Model):
   answer_id = models.IntegerField(primary_key=True, unique=True, verbose_name='ID ответа')
   answer_name = models.CharField(verbose_name='Содержимое ответа')
   question = models.ForeignKey(
      'Question',
      on_delete=models.CASCADE
   )
   service_number = models.ForeignKey(
      'Employee',
      on_delete=models.CASCADE
   )

   class Meta:
      db_table = 'Answer'
      verbose_name = 'Ответ'
      verbose_name_plural = 'Ответы'
