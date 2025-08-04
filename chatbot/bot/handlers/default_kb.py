from aiogram import Bot
from aiogram.types import BotCommand

async def set_default_command(bot: Bot):
   command = [
      BotCommand(command="/askquestion", description="Хочу задать вопрос")
   ]
   await bot.set_my_commands(command)