from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import tell_about_myself_kb # клавиатура
from core.models import *
from asgiref.sync import sync_to_async

start_router = Router()

async def has_completed_registration(telegram_id): #проверяем, проходил ли сотрудник регистрацию
    exists = await sync_to_async(Employee.objects.filter(telegram_id=telegram_id).exists)()
    return exists
    
@start_router.message(CommandStart()) # обработка команды /start
async def cmd_start(message: Message):
    if await has_completed_registration(message.from_user.id):
        await message.answer(
            "Вы уже зарегистрированы в системе!"
        )
    else:
        await message.answer('Мы тебя очень ждали и хотим познакомиться! Расскажи о себе, отвечая на вопросы'
                            ', для этого нажми на кнопку \"Рассказать о себе\".',
                            reply_markup = tell_about_myself_kb(message.from_user.id))