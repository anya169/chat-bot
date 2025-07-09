import aiogram
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType

from config import TOKEN

bot = Bot(token = TOKEN)
dp = Dispatcher()



@dp.message(CommandStart())
async def cmd_start(message: Message):
   await message.answer("""Что умеет это бот?
Приветствую тебя, молодой специалист! 
Я твой личный цифровой помощник, который будет сопровождать тебя на пути профессионального роста. Вместе мы найдем ответы на все интересующие тебя вопросы.

Но для начала давай знакомиться! Напиши ниже /start/ и мы начнем работу!
"""
)

@dp.message(Command('start/'))
async def start_introduction(message: Message):
   await message.answer("""Мы тебя очень ждали и хотим познакомиться! Расскажи о себе, отвечая на вопросы:
"""
)


async def main():
   await dp.start_polling(bot)
   
if __name__ == '__main__':
   try:
      asyncio.run(main())
   except KeyboardInterrupt:
      print('Exit')
   
