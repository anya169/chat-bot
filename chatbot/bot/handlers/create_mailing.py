from aiogram.filters.state import State, StatesGroup
import os
import django
import sys
import asyncio
from asgiref.sync import sync_to_async
from create_bot import bot
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove, ContentType
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters.state import State, StatesGroup
from keyboards import accept_kb, attachment_kb
from aiogram.types import FSInputFile 
from pathlib import Path
from aiogram.types import InputMediaPhoto, InputMediaDocument
from core.models import Employee

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()

class Create_mailing(StatesGroup):
   name = State()
   description = State()
   attachment = State()
   accept = State()
   send = State()

mailing_router = Router()
short_delay = 1

@mailing_router.message(Command('createmailing'))
async def create_mailing(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Созданная вами рассылка будет разослана всем молодым сотрудникам\n\n"
         "Введите название рассылки: ",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.name)

@mailing_router.message(F.text, Create_mailing.name)
async def create_name(message: Message, state: FSMContext):
   await state.update_data(name=message.text)
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Введите описание рассылки: ",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.description)

@mailing_router.message(F.text, Create_mailing.description)
async def create_description(message: Message, state: FSMContext):
   await state.update_data(description=message.text)
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Прикрепите файл или изображение к рассылке. Если хотите добавить несколько вложений, добавляйте каждое отдельным сообщением, а потом подтвердите рассылку.",
         reply_markup=attachment_kb()
      )
   await state.set_state(Create_mailing.attachment)

@mailing_router.message(F.text == "Не прикреплять", Create_mailing.attachment)
async def no_attachment(message: Message, state: FSMContext):
   await state.update_data(attachment=None)
   await show_confirmation(message, state)

@mailing_router.message(
   F.content_type.in_({ContentType.PHOTO, ContentType.DOCUMENT}), 
   Create_mailing.attachment
)
async def process_attachment(message: Message, state: FSMContext):
   try:
      data = await state.get_data()
      attachments = data.get('attachments', [])
      
      #обработка фото
      if message.photo:
         photo = message.photo[-1]
         file = await bot.get_file(photo.file_id)
         os.makedirs("media/mailings", exist_ok=True)
         file_path = f"media/mailings/{photo.file_id}.jpg"
         await bot.download_file(file.file_path, file_path)
         
         attachments.append({
               'type': 'photo',
               'file_id': photo.file_id,
               'path': file_path,
               'telegram_file': file
         })
         
      #обработка документов
      elif message.document:
         doc = message.document
         file = await bot.get_file(doc.file_id)
         os.makedirs("media/mailings", exist_ok=True)
         file_name = doc.file_name or f"document_{doc.file_id}"
         file_path = f"media/mailings/{file_name}"
         await bot.download_file(file.file_path, file_path)
         
         attachments.append({
               'type': 'document',
               'file_id': doc.file_id,
               'path': file_path,
               'file_name': file_name,
               'telegram_file': file
         })
      
      await state.update_data(attachments=attachments)
      
      #сразу показываем подтверждение с текущими вложениями
      await show_confirmation(message, state)
         
   except Exception as e:
      print(f"Ошибка при обработке вложения: {str(e)}")
      await message.answer(
         "Произошла ошибка при обработке файла. Пожалуйста, попробуйте еще раз.",
         reply_markup=attachment_kb()
      )

async def show_confirmation(message: Message, state: FSMContext):
   data = await state.get_data()
   name = data.get('name', '')
   description = data.get('description', '')
   attachments = data.get('attachments', [])
   
   text = (
      f"Подтвердите содержимое рассылки. Если необходимо добавить еще вложения, добавьте по одному следующими после этого сообщения:\n\n"
      f"<b>Название:</b> {name}\n"
      f"<b>Описание:</b> {description}\n"
      f"<b>Количество вложений:</b> {len(attachments)}"
   )
   
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      
      try:
         if attachments:
               media = []
               for i, attachment in enumerate(attachments):
                  file_path = Path(attachment['path'])
                  if attachment['type'] == 'photo':
                     if i == 0:  #подпись только к первому файлу
                           media.append(InputMediaPhoto(
                              media=FSInputFile(file_path),
                              caption=text,
                              parse_mode="HTML"
                           ))
                     else:
                           media.append(InputMediaPhoto(
                              media=FSInputFile(file_path)
                           ))
                  elif attachment['type'] == 'document':
                     if i == 0:
                           media.append(InputMediaDocument(
                              media=FSInputFile(file_path, filename=attachment.get('file_name', file_path.name)),
                              caption=text,
                              parse_mode="HTML"
                           ))
                     else:
                           media.append(InputMediaDocument(
                              media=FSInputFile(file_path, filename=attachment.get('file_name', file_path.name))
                           ))
               
               #отправляем все вложения одним медиагруппом
               await message.answer_media_group(media=media)
               await message.answer(
                  "Подтвердите рассылку:",
                  reply_markup=accept_kb()
               )
         else:
               await message.answer(
                  text,
                  reply_markup=accept_kb(),
                  parse_mode="HTML"
               )
               
      except Exception as e:
         print(f"Ошибка при показе подтверждения: {str(e)}")
         await message.answer(
               "Не удалось отобразить вложения. Пожалуйста, попробуйте отправить файлы еще раз.",
               reply_markup=attachment_kb()
         )
         await state.set_state(Create_mailing.attachment)
         return
   
   await state.set_state(Create_mailing.accept)

@mailing_router.message(F.text == "Подтвердить", Create_mailing.accept)
async def send_mailing(message: Message, state: FSMContext):
   data = await state.get_data()
   name = data.get('name', '')
   description = data.get('description', '')
   attachments = data.get('attachments', [])
   
   employees = await sync_to_async(list)(
      Employee.objects.exclude(telegram_id__isnull=True).filter(is_curator=False, is_admin=False)
   )
   
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         f"Начинаю рассылку для {len(employees)} сотрудников...",
         reply_markup=ReplyKeyboardRemove()
      )
   
   success_count = 0
   for employee in employees:
      try:
         if attachments:
               media = []
               for i, attachment in enumerate(attachments):
                  file_path = Path(attachment['path'])
                  if attachment['type'] == 'photo':
                     if i == 0:  #подпись только к первому файлу
                           media.append(InputMediaPhoto(
                              media=FSInputFile(file_path),
                              caption=f"<b>{name}</b>\n\n{description}",
                              parse_mode="HTML"
                           ))
                     else:
                           media.append(InputMediaPhoto(
                              media=FSInputFile(file_path)
                           ))
                  elif attachment['type'] == 'document':
                     if i == 0:
                           media.append(InputMediaDocument(
                              media=FSInputFile(file_path, filename=attachment.get('file_name', file_path.name)),
                              caption=f"<b>{name}</b>\n\n{description}",
                              parse_mode="HTML"
                           ))
                     else:
                           media.append(InputMediaDocument(
                              media=FSInputFile(file_path, filename=attachment.get('file_name', file_path.name))
                           ))
               
               #отправляем все вложения одним медиагруппом
               await bot.send_media_group(
                  chat_id=employee.telegram_id,
                  media=media
               )
         else:
               await bot.send_message(
                  chat_id=employee.telegram_id,
                  text=f"<b>{name}</b>\n\n{description}",
                  parse_mode="HTML"
               )
         success_count += 1
         await asyncio.sleep(0.1)
      except Exception as e:
         print(f"Ошибка при отправке сотруднику {employee.telegram_id}: {e}")
   
   await message.answer(
      f"Рассылка завершена! Успешно отправлено для {success_count} из {len(employees)} сотрудников."
   )
   await state.clear()

@mailing_router.message(F.text == "Отредактировать", Create_mailing.accept)
async def edit_mailing(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Введите новое название рассылки: ",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.name)