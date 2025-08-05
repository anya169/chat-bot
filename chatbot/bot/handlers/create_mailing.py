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
from aiogram.exceptions import TelegramBadRequest

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
         "Введите название рассылки",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.name)

@mailing_router.message(F.text, Create_mailing.name)
async def create_name(message: Message, state: FSMContext):
   await state.update_data(name=message.text)
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Введите описание рассылки",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.description)

@mailing_router.message(F.text, Create_mailing.description)
async def create_description(message: Message, state: FSMContext):
   await state.update_data(description=message.text)
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Прикрепите файл или изображение к рассылке",
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
      if message.photo:
         file = await bot.get_file(message.photo[-1].file_id)
         os.makedirs("media", exist_ok=True)
         file_path = f"media/{file.file_id}.jpg"
         await bot.download_file(file.file_path, file_path)
         await state.update_data(attachment={
               'type': 'photo', 
               'path': file_path,
               'file_id': message.photo[-1].file_id  
         })
      elif message.document:
         file_id = message.document.file_id
         # Для документов сразу скачиваем файл
         file = await bot.get_file(file_id)
         os.makedirs("media", exist_ok=True)
         file_path = f"media/{file_id}_{message.document.file_name}"
         await bot.download_file(file.file_path, file_path)
         await state.update_data(attachment={
               'type': 'document', 
               'file_id': file_id,
               'path': file_path,
               'file_name': message.document.file_name
         })
      
      await show_confirmation(message, state)
   except TelegramBadRequest as e:
      await message.answer("Произошла ошибка при обработке файла. Пожалуйста, попробуйте еще раз.")
      await state.set_state(Create_mailing.attachment)

async def show_confirmation(message: Message, state: FSMContext):
   data = await state.get_data()
   name = data.get('name', '')
   description = data.get('description', '')
   attachment = data.get('attachment')
   
   text = (
      f"Подтвердите содержимое рассылки:\n\n"
      f"<b>Название:</b> {name}\n"
      f"<b>Описание:</b> {description}\n"
      f"<b>Вложение:</b> {'есть' if attachment else 'нет'}"
   )
   
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      
      try:
         if attachment and attachment['type'] == 'photo':
               with open(attachment['path'], 'rb') as photo:
                  await message.answer_photo(
                     photo=photo,
                     caption=text,
                     reply_markup=accept_kb(),
                     parse_mode="HTML"
                  )
         elif attachment and attachment['type'] == 'document':
               with open(attachment['path'], 'rb') as doc:
                  await message.answer_document(
                     document=doc,
                     caption=text,
                     reply_markup=accept_kb(),
                     parse_mode="HTML"
                  )
         else:
               await message.answer(
                  text,
                  reply_markup=accept_kb(),
                  parse_mode="HTML"
               )
      except Exception as e:
         await message.answer(
               "Не удалось отобразить вложение. Пожалуйста, попробуйте еще раз.",
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
   attachment = data.get('attachment')
   
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
         if attachment and attachment['type'] == 'photo':
               with open(attachment['path'], 'rb') as photo:
                  await bot.send_photo(
                     chat_id=employee.telegram_id,
                     photo=photo,
                     caption=f"<b>{name}</b>\n\n{description}",
                     parse_mode="HTML"
                  )
         elif attachment and attachment['type'] == 'document':
               with open(attachment['path'], 'rb') as doc:
                  await bot.send_document(
                     chat_id=employee.telegram_id,
                     document=doc,
                     caption=f"<b>{name}</b>\n\n{description}",
                     parse_mode="HTML"
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
         "Введите новое название рассылки",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Create_mailing.name)