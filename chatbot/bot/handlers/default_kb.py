from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeChat, BotCommandScopeDefault
from create_bot import get_curators_telegram_ids

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
   curators = await get_curators_telegram_ids()
   print(f"Кураторы: {curators}")
   if curators:
      for curator in curators:
         await bot.set_my_commands(
                     commands=admin_command,
                     scope=BotCommandScopeChat(chat_id=curator) 
                  )