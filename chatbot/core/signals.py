from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Special_Question
from asgiref.sync import async_to_sync
from aiogram import Bot
import asyncio

bot_instance = None
bot_lock = asyncio.Lock()

async def get_bot():
    global bot_instance
    if bot_instance is None:
        bot_instance = Bot('7741930969:AAFFBhqYEqetYvSKCHtKSQ5yhP1mUNNHwo8')
    return bot_instance

@receiver(post_save, sender = Special_Question)
def send_answer_to_user(sender, instance, created, **kwargs):
    if not created and instance.answer:
        employee = instance.employee_id
        if employee and employee.telegram_id:
            message = (
                f"У вас новый ответ на вопрос!\n\n"
                f"Ваш вопрос: {instance.name}\n"
                f"Ответ: {instance.answer}"
            )
            async def async_send():
                try:
                    async with bot_lock:
                        bot = await get_bot()
                        await bot.send_message(
                            chat_id = employee.telegram_id,
                            text=message
                        )
                except Exception as e:
                    print(f"Ошибка при отправке сообщения: {e}")
                    global bot_instance
                    if bot_instance:
                        await bot_instance.close()
                    bot_instance = None
            async_to_sync(async_send)()