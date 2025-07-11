import aiogram

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType

import keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
   await message.reply("""Что умеет это бот?
Приветствую тебя, молодой специалист! 
Я твой личный цифровой помощник, который будет сопровождать тебя на пути профессионального роста. Вместе мы найдем ответы на все интересующие тебя вопросы.

Но для начала давай знакомиться! Напиши ниже /start/ и мы начнем работу!
""", 
   reply_markup=kb.start
)

@router.message(Command('start'))
@router.message(lambda message: message.text == "ЗАПУСТИТЬ")
async def start_introduction(message: Message):
   await message.answer("""Мы тебя очень ждали и хотим познакомиться! Расскажи о себе, отвечая на вопросы:
"""
)
