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
        today = datetime.now().date()
        days_employed = (today - employee.hire_date).days
        logger.info(f"Сотрудник {employee.id}, работает {days_employed} дней")
                
        if days_employed < 30:
            if await is_user_available(employee.telegram_id):
                schedule_poll(scheduler, employee, 30, send_poll_after_1_month)
                schedule_poll(scheduler, employee, 90, send_poll_after_3_month)
                schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
                schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
        
        # Для работающих 1-3 месяца
        elif 30 <= days_employed < 90:
            if await is_user_available(employee.telegram_id):
                schedule_poll(scheduler, employee, 90, send_poll_after_3_month)
                schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
                schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
        
        # Для работающих 3-6 месяцев
        elif 90 <= days_employed < 180:
            if await is_user_available(employee.telegram_id):
                schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
                schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
        
        # Для работающих 6-12 месяцев 
        elif 180 <= days_employed < 365:
            if await is_user_available(employee.telegram_id):
                schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
                
        # Для работающих больше года       
        else:
                
            if await is_user_available(employee.telegram_id):
                schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
                
    
    logger.info(f"Scheduled polls for employee {employee.id}")