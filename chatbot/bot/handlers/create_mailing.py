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
from core.models import Employee, Mailing, MailingAttachment
from django.core.files import File
from datetime import datetime
from django.conf import settings

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()

class Create_mailing(StatesGroup):
   tag = State()
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
         "Созданная вами рассылка будет отображаться на сайте\n\n"
         "Введите тег рассылки: ",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.tag)

@mailing_router.message(F.text, Create_mailing.tag)
async def create_name(message: Message, state: FSMContext):
   await state.update_data(tag=message.text)
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
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
         media_dir = os.path.join(settings.MEDIA_ROOT, "mailings")
         file_name = f"{photo.file_id}.jpg"
         full_path = os.path.join(media_dir, file_name)
         relative_path = os.path.join("mailings", file_name)
         await bot.download_file(file.file_path, full_path)
         
         attachments.append({
               'type': 'photo',
               'file_id': photo.file_id,
               'file_name': file_name,
               'path': relative_path,
               'telegram_file': file,
               'full_path': full_path
         })
         
      #обработка документов
      elif message.document:
         doc = message.document
         file = await bot.get_file(doc.file_id)
         media_dir = os.path.join(settings.MEDIA_ROOT, "mailings")
         file_name = doc.file_name or f"document_{doc.file_id}"
         full_path = os.path.join(media_dir, file_name)
         relative_path = os.path.join("mailings", file_name)
         await bot.download_file(file.file_path, full_path)
         
         attachments.append({
               'type': 'document',
               'file_id': doc.file_id,
               'path': relative_path,
               'file_name': file_name,
               'full_path': full_path,
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
   tag = data.get('tag', '')
   name = data.get('name', '')
   description = data.get('description', '')
   attachments = data.get('attachments', [])
   
   text = (
      f"Подтвердите содержимое рассылки. Если необходимо добавить еще вложения, нажмите Добавить еще файлы:\n\n"
      f"<b>Тег:</b> {tag}\n"
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
                  file_path = attachment['full_path']
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
                              media=FSInputFile(file_path),
                              caption=text,
                              parse_mode="HTML",
                              filename=attachment['file_name']
                           ))
                     else:
                           media.append(InputMediaDocument(
                              media=FSInputFile(file_path, attachment['file_name'])
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
               "Не удалось отобразить вложения. Все вложения должны быть одного типа (только документы или только изображения). Пожалуйста, попробуйте еще раз. Введите новый тег рассылки: ",
               reply_markup=ReplyKeyboardRemove()
         )
         data['attachments'] = [] 
         await state.update_data(attachments=[])
         await state.set_state(Create_mailing.tag)
         return
   
   await state.set_state(Create_mailing.accept)
   
@mailing_router.message(F.text == "Добавить ещё файлы", Create_mailing.accept)
async def add_more_files(message: Message, state: FSMContext):
   await message.answer(
      "Все вложения должны быть одного типа (только документы или только изображения). Прикрепите дополнительные файлы:",
      reply_markup=attachment_kb()
   )
   await state.set_state(Create_mailing.attachment)
    
@mailing_router.message(F.text == "Подтвердить", Create_mailing.accept)
async def send_mailing(message: Message, state: FSMContext):
   data = await state.get_data()
   attachments = data.get('attachments', [])
   
   # Сохраняем рассылку
   mailing = Mailing(
      tag=data.get('tag'),
      name=data.get('name'),
      employee_id=(await sync_to_async(Employee.objects.get)(telegram_id=message.from_user.id)).id,
      description=data.get('description')
   )
   await sync_to_async(mailing.save)()
   
   # Сохраняем вложения
   for attachment in attachments:
      try:
         file_path = attachment['full_path']
         
         if not os.path.exists(file_path):
               print(f"Файл не найден: {file_path}")
               continue
               
         with open(file_path, 'rb') as f:
               django_file = File(f, name=os.path.basename(file_path)) 
               mailing_attachment = MailingAttachment(
                  mailing=mailing,
                  file=django_file,
                  file_type=attachment['type'],
                  file_name=attachment['file_name']  
               )
               await sync_to_async(mailing_attachment.save)()
               
      except Exception as e:
         print(f"Ошибка сохранения вложения: {e}")
         continue
   
   await message.answer("Рассылка сохранена!", reply_markup=ReplyKeyboardRemove())
   await state.clear()
    
@mailing_router.message(F.text == "Отредактировать", Create_mailing.accept)
async def edit_mailing(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Введите новый тег рассылки: ",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.tag)

