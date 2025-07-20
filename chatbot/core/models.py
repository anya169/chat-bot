from django.db import models

class Employee(models.Model):
   objects = models.Manager()
   
   num_tab = models.CharField(max_length=200, null=True, blank=True, verbose_name='Табельный номер')
   name = models.CharField(max_length=200, null=True, blank=True, verbose_name='ФИО')
   post = models.CharField(max_length=200, null=True, blank=True, verbose_name='Должность')
   email = models.CharField(max_length=200, null=True, blank=True, verbose_name='Почта')
   filial = models.ForeignKey('Filial', null=True, blank=True, related_name='users', on_delete=models.DO_NOTHING, verbose_name='Филиал')
   struct = models.ForeignKey('Struct', null=True, blank=True, related_name='users', on_delete=models.DO_NOTHING, verbose_name='Подразделение')
   login = models.CharField(max_length=200, null=True, blank=True, verbose_name='Логин')
   is_del = models.BooleanField(default=False, verbose_name='Уволен')
   is_admin = models.BooleanField(default=False, verbose_name='Администратор')
   is_can_manage_global_groups = models.BooleanField(default=False, verbose_name='Может управлять глобальными группами')
   is_can_view_all_forms = models.BooleanField(default=False, verbose_name='Может просматривать все формы')
   is_curator = models.BooleanField(default=False, verbose_name='Является ли куратором')
   telegram_id = models.IntegerField(null=True, blank=True, verbose_name="Telegram ID")
   hire_date = models.DateField(null=True, blank=True, verbose_name="Дата приёма на работу")
   telegram_registration_date = models.DateField(null=True, blank=True, auto_now_add=True, verbose_name="Дата первого обращения к боту")
   curator_login = models.CharField(max_length=200, null=True, blank=True, verbose_name='Логин куратора')

   def __str__(self):
      return self.name

   class Meta:
      db_table = 'Employee'
      verbose_name = "Сотрудник"
      verbose_name_plural = "Сотрудники"


class Struct(models.Model):
   objects = models.Manager()
   
   name = models.CharField(max_length=100, null=True, blank=True, verbose_name="Название подразделения")
  
   def __str__(self):
      return self.name
  
   class Meta:
      db_table = 'Struct'
      verbose_name = "Подразделение"
      verbose_name_plural = "Подразделения"
      
class Poll(models.Model):
   objects = models.Manager()
   
   name = models.CharField(null=True, blank=True, verbose_name='Название опроса')
   description = models.CharField(null=True, blank=True,verbose_name='Описание опроса')   
   duration = models.DurationField(null=True,  blank=True, verbose_name='Время, через которое запускается опрос')
   submission_date = models.DurationField(null=True, blank=True, verbose_name='Дата создания')
   is_unexpected = models.BooleanField(default=False, verbose_name='Является ли внеплановым') 
        

   def __str__(self):
      return self.name
   
   class Meta:
      db_table = 'Poll'
      verbose_name = 'Опрос'
      verbose_name_plural = 'Опросы'

class Filial(models.Model):
   objects = models.Manager()
   
   name = models.TextField(max_length=1000, null=True, blank=True, verbose_name='Название')

   def __str__(self):
      return self.name

   class Meta:
      verbose_name = "Филиал"
      verbose_name_plural = "Филиалы"
      db_table = 'Filial'

class Question(models.Model):
   objects = models.Manager()
   
   name = models.CharField(null=True, blank=True, verbose_name='Название вопроса')
   poll = models.ForeignKey(
      'Poll',
      on_delete=models.CASCADE
   )
   
   def __str__(self):
      return self.name
   
   class Meta:
      db_table = 'Question'
      verbose_name = 'Вопрос'
      verbose_name_plural = 'Вопросы'


class Answer(models.Model):
   objects = models.Manager()
   
   name = models.CharField(null=True, blank=True, verbose_name='Содержимое ответа')
   submission_date = models.DurationField(null=True, blank=True, verbose_name='Дата создания')
   question = models.ForeignKey(
      'Question',
      on_delete=models.CASCADE
   )
   login = models.ForeignKey(
      'Employee',
      on_delete=models.CASCADE
   )

   def __str__(self):
      return self.name
   
   class Meta:
      db_table = 'Answer'
      verbose_name = 'Ответ'
      verbose_name_plural = 'Ответы'

class Special_Question(models.Model):
   objects = models.Manager()
   
   name = models.CharField(null=True, blank=True, verbose_name='Название вопроса')
   answer = models.CharField(null=True, blank=True, verbose_name='Ответ на вопрос')
   submission_date = models.DurationField(null=True, blank=True, verbose_name='Дата создания')
   employee = models.ForeignKey('Employee', null=True, blank=True, related_name='users', on_delete=models.DO_NOTHING, verbose_name='ID')

   
   def __str__(self):
      return self.name
   
   class Meta:
      db_table = 'Special_Question'
      verbose_name = 'Специальный вопрос'
      verbose_name_plural = 'Специальные вопросы'