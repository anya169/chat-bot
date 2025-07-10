import aiogram

from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType


router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
   await message.answer("""Что умеет это бот?
Приветствую тебя, молодой специалист! 
Я твой личный цифровой помощник, который будет сопровождать тебя на пути профессионального роста. Вместе мы найдем ответы на все интересующие тебя вопросы.

Но для начала давай знакомиться! Напиши ниже /start/ и мы начнем работу!
"""
)

@router.message(Command('start/'))
async def start_introduction(message: Message):
   await message.answer("""Мы тебя очень ждали и хотим познакомиться! Расскажи о себе, отвечая на вопросы:
"""
)

