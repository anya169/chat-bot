from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from asgiref.sync import sync_to_async
from core.models import Mailing, MailingAttachment, Employee
from pathlib import Path
from aiogram.types import InputMediaPhoto, InputMediaDocument, FSInputFile
from bot.create_bot import bot
import asyncio

@csrf_exempt
def send_mailing_to_employee(request):
   try:
      data = json.loads(request.body)
      #получаем айди рассылки и сотрудников
      mailing_id = data.get('mailing_id')
      employee_ids = data.get('employee_ids', [])
         
      mailing = Mailing.objects.get(id=mailing_id)
      attachments = MailingAttachment.objects.filter(mailing=mailing)
      employees = Employee.objects.filter(id__in=employee_ids, telegram_id__isnull=False)
      
      if not employees.exists():
         return JsonResponse({'error': 'Не найдено сотрудников с Telegram ID'}, status=400)
      
      #запускаем асинхронную отправку в отдельном потоке
      import threading
      
      #считаем количество отправленных сообщений и нет
      result = {'success_count': 0, 'error_count': 0}
      
      def send_in_thread():
         loop = asyncio.new_event_loop()
         asyncio.set_event_loop(loop)
         try:
            thread_result = loop.run_until_complete(
               send_mailing_async(mailing, attachments, employees)
            )
            result.update(thread_result)
         finally:
            loop.close()
      
      #запускаем в отдельном потоке
      thread = threading.Thread(target=send_in_thread)
      thread.start()
      thread.join()  
      
      return JsonResponse(result)
      
   except Mailing.DoesNotExist:
      return JsonResponse({'error': 'Рассылка не найдена'}, status=404)
   except json.JSONDecodeError:
      return JsonResponse({'error': 'Неверный JSON'}, status=400)
   except Exception as e:
      return JsonResponse({'error': str(e)}, status=500)


async def send_mailing_async(mailing, attachments, employees):
   success_count = 0
   error_count = 0
   
   #преобразуем в списки для асинхронной работы
   attachments_list = await sync_to_async(list)(attachments)
   employees_list = await sync_to_async(list)(employees)  
   
   media = []
   
   for i, attachment in enumerate(attachments_list):
      try:
         file_path = Path(attachment.file.path)
         
         file_exists = await sync_to_async(file_path.exists)()
         if not file_exists:
               print(f"Файл не найден: {file_path}")
               error_count += 1
               continue
               
         #создаем медиа объект
         if attachment.file_type == 'photo':
               media_item = InputMediaPhoto(media=FSInputFile(file_path))
         else:
               media_item = InputMediaDocument(media=FSInputFile(file_path))
         
         if i == 0:
               media_item.caption = f"<b>{mailing.name}</b>\n\n{mailing.description}"
               media_item.parse_mode = "HTML"
         
         media.append(media_item)
         
      except Exception as e:
         print(f"Ошибка обработки вложения: {e}")
         error_count += 1
         continue
   
   #отправляем сообщения
   for employee in employees_list: 
      try:
         print(f"Отправка сотруднику {employee.telegram_id}")
         
         if media:
               await bot.send_media_group(
                  chat_id=employee.telegram_id,
                  media=media
               )
         else:
               await bot.send_message(
                  chat_id=employee.telegram_id,
                  text=f"<b>{mailing.name}</b>\n\n{mailing.description}",
                  parse_mode="HTML"
               )
         success_count += 1
         await asyncio.sleep(0.1)
         
      except Exception as e:
         print(f"Ошибка при отправке сотруднику {employee.telegram_id}: {e}")
         from bot.config import add_to_blocked
         add_to_blocked(employee.telegram_id)
         error_count += 1
         continue
   
   print(f"Итог: Успешно {success_count}, Ошибок {error_count}")
   return {
      'success_count': success_count,
      'error_count': error_count
   }