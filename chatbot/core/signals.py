from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from decouple import config
from aiogram import Bot
from core.models import Employee, Special_Question
import logging
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
logger = logging.getLogger(__name__)
from bot.scheduler import is_user_available


bot = None
def get_bot():
    bot =  Bot(token=config('TOKEN'))
    return bot


@receiver(post_save, sender=Special_Question)
def send_answer_to_user(sender, instance, created, **kwargs):
    if not created and instance.answer and hasattr(instance, 'employee'):
        print(f"New special q")
        employee = instance.employee
        if employee and employee.telegram_id:
            message = (
                f"У вас новый ответ на вопрос!\n\n"
                f"Ваш вопрос: {instance.name}\n"
                f"Ответ: {instance.answer}"
            )
            async_to_sync(async_send_message)(employee.telegram_id, message)

async def async_send_message(chat_id, text):
    bot = get_bot()
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        raise

@receiver(post_save, sender=Employee)
def handle_new_employee(sender, instance, created, **kwargs):
    if created:
        print(f"New employee signal received for {instance.id}")
          