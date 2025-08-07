from django.db.models.signals import post_save
from django.dispatch import receiver
from core.models import Special_Question
from aiogram import Bot
from asgiref.sync import async_to_sync

bot = None

def get_bot():
    global bot
    if bot is None:
        bot = Bot('7741930969:AAFFBhqYEqetYvSKCHtKSQ5yhP1mUNNHwo8')
    return bot

@receiver(post_save, sender=Special_Question)
def send_answer_to_user(sender, instance, created, **kwargs):
    if not created and instance.answer and hasattr(instance, 'employee'):
        employee = instance.employee
        if employee and employee.telegram_id:
            message = (
                f"У вас новый ответ на вопрос!\n\n"
                f"Ваш вопрос: {instance.name}\n"
                f"Ответ: {instance.answer}"
            )
            
            async_to_sync(async_send_message)(employee.telegram_id, message)

async def async_send_message(chat_id, text):
    try:
        bot = get_bot()
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка в async_send_message: {e}")
        bot
        if bot:
            await bot.close()
            bot = None
        raise