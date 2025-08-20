from django.contrib import admin
from core.models import *
from django.utils.html import format_html

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
   list_display = ('name', 'login',  'is_curator', 'curator_login', 'telegram_id', 'hire_date', 'telegram_registration_date')
   list_filter = ('is_curator', 'hire_date', 'telegram_registration_date', 'curator_login')
   search_fields = ('name', 'login', 'telegram_id')
   ordering = ('name', 'filial')
   actions = ['send_1_month_poll']

   
   @admin.action(description="Отправить опрос через 1 месяц")
   def send_1_month_poll(self, request, queryset):
      from bot.create_bot import bot, dp
      from django.contrib import messages
      import asyncio
      import logging
      logger = logging.getLogger(__name__)
      async def async_send_wrapper(employee_id):
         try:
            from bot.scheduler import send_poll_after_1_month
            return await send_poll_after_1_month(employee_id)
         except Exception as e:
            logger.error(f"Ошибка в wrapper: {str(e)}", exc_info=True)
            return False

      def sync_send_wrapper(employee_id):
         loop = asyncio.new_event_loop()
         asyncio.set_event_loop(loop)
         try:
               result = loop.run_until_complete(async_send_wrapper(employee_id))
               return result
         except Exception as e:
               logger.error(f"Ошибка в синхронной обёртке: {str(e)}", exc_info=True)
               return False
         finally:
               loop.close()

      for employee in queryset:
         if not employee.telegram_id:
               messages.warning(request, f"Нет telegram_id у {employee.name}")
               continue
               
         try:
               result = sync_send_wrapper(employee.id)
               if result is True:
                  messages.success(request, f"Успешно отправлено: {employee.name}")
               else:
                  messages.error(request, f"Не удалось отправить: {employee.name}")
         except Exception as e:
               messages.error(request, f"Критическая ошибка для {employee.name}: {str(e)}")
               
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
   
@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
   list_display = ('name', 'login_id', 'question_id', 'get_poll_name')
   def get_poll_name(self, obj):
      return obj.question.poll.name if obj.question.poll else '-'
   get_poll_name.short_description = 'Опрос'  
   get_poll_name.admin_order_field = 'poll__name'
   list_filter = ('submission_date', 'question_id')
   search_fields = ('login_id', 'question_id')  
   ordering = ('submission_date', )
   
@admin.register(Mailing)
class MailingAdmin(admin.ModelAdmin):   
   list_display = ('name', 'description', 'creation_date', 'get_curator_name', 'get_attachments_list')
   def get_curator_name(self, obj):
      return obj.employee.name if obj.employee else '-'
   get_curator_name.short_description = 'Куратор'  
   get_curator_name.admin_order_field = 'employee__name'
   def get_attachments_list(self, obj):
      attachments = obj.attachments.all()  # Используем related_name='attachments'
      if attachments:
         return format_html(
               "<ul>{}</ul>".format(
                  "".join([
                     f"<li>{attachment.file_name or attachment.file.name}</li>" 
                     for attachment in attachments
                  ])
               )
         )
      return "-"
   get_attachments_list.short_description = 'Вложения'
   get_attachments_list.allow_tags = True
   search_fields = ('name', 'creation_date')
   ordering = ('creation_date', )   
   list_filter = ('creation_date', 'employee_id')
   
@admin.register(Filial)
class FilialAdmin(admin.ModelAdmin):   
   list_display = ('name', )
   search_fields = ('name', )

@admin.register(Struct)
class StructAdmin(admin.ModelAdmin):   
   list_display = ('name', )
   search_fields = ('name', )
   
@admin.register(Special_Question)
class Special_QuestionAdmin(admin.ModelAdmin):   
   list_display = ('name', 'answer', 'get_employee_name', 'creation_answer', 'creation_question')
   def get_employee_name(self, obj):
      return obj.employee.name if obj.employee else '-'
   get_employee_name.short_description = 'Сотрудник'  
   get_employee_name.admin_order_field = 'employee__name'
   
