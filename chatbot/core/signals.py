from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from decouple import config
from aiogram import Bot
from core.models import Employee, Special_Question
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler

logger = logging.getLogger(__name__)

_bot_instance = None

def get_bot():
    global _bot_instance
    if _bot_instance is None:
        _bot_instance = Bot('7741930969:AAFFBhqYEqetYvSKCHtKSQ5yhP1mUNNHwo8')
    return _bot_instance

async def close_bot():
    global _bot_instance
    if _bot_instance:
        await _bot_instance.close()
        _bot_instance = None

_scheduler_instance = None

def get_scheduler():
    global _scheduler_instance
    if _scheduler_instance is None:
        _scheduler_instance = AsyncIOScheduler(timezone='Europe/Moscow')
        _scheduler_instance.start()
    return _scheduler_instance

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
    bot = get_bot()
    try:
        await bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        logger.error(f"Error sending Telegram message: {e}")
        raise
    finally:
        await close_bot()
        
@receiver(post_save, sender=Employee)
def handle_new_employee(sender, instance, created, **kwargs):
    if created and instance.hire_date:
        logger.info(f"New employee signal received for {instance.id}")
        try:
            # Запускаем асинхронную задачу для планирования опросов
            async_to_sync(schedule_employee_polls)(instance)
        except Exception as e:
            logger.error(f"Error scheduling polls: {e}", exc_info=True)
            raise

async def schedule_employee_polls(employee):
    from bot.scheduler import (
        schedule_poll,
        send_poll_after_1_month,
        send_poll_after_3_month,
        send_poll_after_6_month,
        send_poll_after_12_month
    )
    
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    if not scheduler.running:
        scheduler.start()
    
    schedule_poll(scheduler, employee, 30, send_poll_after_1_month)
    schedule_poll(scheduler, employee, 90, send_poll_after_3_month)
    schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
    schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
    
    logger.info(f"Scheduled polls for employee {employee.id}")