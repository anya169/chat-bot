from aiogram import Bot
from aiogram.types import ChatMemberRestricted, ChatMemberLeft, ChatMemberBanned

async def get_blocked_users(bot: Bot, user_ids: list):
   blocked_users = []
   
   for user_id in user_ids:
      try:
         chat_member = await bot.get_chat_member(chat_id=user_id, user_id=user_id)
         
         # Проверяем статус пользователя
         if isinstance(chat_member, (ChatMemberLeft, ChatMemberBanned, ChatMemberRestricted)):
            blocked_users.append(user_id)
               
      except Exception as e:
         # Если ошибка "user not found" или "bot was blocked" - пользователь заблокировал бота
         error_msg = str(e).lower()
         if any(phrase in error_msg for phrase in ['user not found', 'bot was blocked', 'chat not found', 'forbidden']):
            blocked_users.append(user_id)
   
   return blocked_users
