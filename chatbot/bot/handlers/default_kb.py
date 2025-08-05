from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from create_bot import admins

async def set_default_command(bot: Bot):
   command = [
      BotCommand(command="askquestion", description="Хочу задать вопрос")
   ]
   await bot.set_my_commands(
      commands=command,
      scope=BotCommandScopeDefault()  #для всех пользователей по умолчанию
   )
   admin_command = [
      BotCommand(command="createmailing", description="Создать рассылку")
   ]
   print(f"Админские ID: {admins}")
   for admin in admins:
      await bot.set_my_commands(
                  commands=admin_command,
                  scope=BotCommandScopeChat(chat_id=admin) 
               )