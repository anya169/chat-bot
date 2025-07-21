from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import tell_about_myself_kb # клавиатура

start_router = Router()

@start_router.message(CommandStart()) # обработка команды /start
async def cmd_start(message: Message):
    await message.answer('Мы тебя очень ждали и хотим познакомиться! Расскажи о себе, отвечая на вопросы'
                         ', для этого нажми на кнопку \"Рассказать о себе\".',
                         reply_markup = tell_about_myself_kb(message.from_user.id))