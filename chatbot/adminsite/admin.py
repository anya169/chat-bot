from django.contrib import admin
from core.models import *

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
   list_display = ('name', 'login',  'is_curator', 'curator_login', 'telegram_id', 'hire_date', 'telegram_registration_date')
   list_filter = ('is_curator', 'hire_date', 'telegram_registration_date', 'curator_login')
   search_fields = ('name', 'login', 'telegram_id')
   ordering = ('name', 'filial')
   
@admin.register(Poll)
class PollAdmin(admin.ModelAdmin):   
   list_display = ('name', 'submission_date')
   search_fields = ('name', )
   ordering = ('submission_date', )
   
@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
   list_display = ('name', 'get_poll_name')
   def get_poll_name(self, obj):
      return obj.poll.name if obj.poll else '-'
   get_poll_name.short_description = 'Опрос'  
   get_poll_name.admin_order_field = 'poll__name'