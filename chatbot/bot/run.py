import aiogram
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, ContentType

from config import TOKEN
from handlers import router

bot = Bot(token = TOKEN)
dp = Dispatcher()

async def main():
   dp.include_router(router)
   await dp.start_polling(bot)
   
if __name__ == '__main__':
   try:
      asyncio.run(main())
   except KeyboardInterrupt:
      print('Exit')
   
