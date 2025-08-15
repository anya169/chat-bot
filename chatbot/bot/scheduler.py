import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from create_bot import bot, dp 
from core.models import *
from asgiref.sync import sync_to_async
from bot.handlers.after_1_month import Form_1
from bot.handlers.after_3_month import Form_3
from bot.handlers.after_6_month import Form_6
from bot.handlers.after_12_month import Form_12
from bot.keyboards import ready_kb
import logging
from channels.db import database_sync_to_async

async def has_completed_poll(employee_id, poll_name):
    try:
        poll = await database_sync_to_async(Poll.objects.get)(name=poll_name)
        queryset = Answer.objects.filter(login_id=employee_id, question__poll=poll)
        exists = await sync_to_async(queryset.exists)()
        return exists
    except Poll.DoesNotExist:
        return False


# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def is_user_available(telegram_id):
    try:
        current_state = await dp.fsm.get_context(
            bot=bot,
            chat_id=telegram_id,
            user_id=telegram_id
        ).get_state()
        return current_state is None
    except Exception as e:
        logger.error(f"Ошибка при проверке состояния пользователя {telegram_id}: {e}")
        return False

async def send_poll_after_1_month(employee_id):
    if (not await has_completed_poll(employee_id, "Опрос через месяц")): #если сотрудник еще не проходил опрос
        try:
            employee = await database_sync_to_async(Employee.objects.get)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 1 месяц отложен")
                return
            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_1.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\nПоздравляем с первым месяцем в команде!\n\n'
                    'Чтобы оценить, как идут дела, предлагаем пройти опрос по чек-листу.\n\n'
                    'Готов(а)? Нажимай кнопку «Готов(а)»',
                reply_markup=await ready_kb(employee.telegram_id)
            )
            logger.info(f"Установлено состояние: {await state.get_state()}")
            logger.info(f"Опрос через 1 месяц отправлен сотруднику {employee_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке опроса через 1 месяц сотруднику {employee_id}: {e}")

async def send_poll_after_3_month(employee_id):
    """Отправляет опрос через 3 месяца после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 3 месяца")): #если сотрудник еще не проходил опрос
        try:
            employee = await database_sync_to_async(Employee.objects.get)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 3 месяца отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_3.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                    'Три месяца в компании — отличный результат!\n\n'
                    'Твой адаптационный период подходит к концу, и мне важно узнать, '
                    'как у тебя идут дела. Поделись своими впечатлениями, пожалуйста, '
                    'ответив на предложенные вопросы.\n\n'
                    'Готов(а)? Нажимай кнопку «Готов(а)»',
                reply_markup=await ready_kb(employee.telegram_id)
            )
            logger.info(f"Опрос через 3 месяца отправлен сотруднику {employee_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке опроса через 3 месяца сотруднику {employee_id}: {e}")

async def send_poll_after_6_month(employee_id):
    """Отправляет опрос через 6 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 6 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await database_sync_to_async(Employee.objects.get)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 6 месяцев отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_6.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                    'Поздравляю с достижением экватора трудового стажа в нашей компании! '
                    'За этот год ты, несомненно, приобрел немало знаний и опыта.\n\n'
                    'Поделишься, как продвигается твоя работа? Ответы на наши вопросы помогут нам лучше понять твою ситуацию.\n\n'
                    'Готов(а)? Нажимай кнопку «Готов(а)»',
                reply_markup=await ready_kb(employee.telegram_id)
            )
            logger.info(f"Опрос через 6 месяцев отправлен сотруднику {employee_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке опроса через 6 месяцев сотруднику {employee_id}: {e}")
            
async def send_poll_after_12_month(employee_id):
    """Отправляет опрос через 12 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 12 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await database_sync_to_async(Employee.objects.get)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 12 месяцев отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_12.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                           'Поздравляю с первым трудовым годом в нашей замечательной команде! '
                           'За прошедший год ты стал важной частью коллектива, внес огромный вклад в развитие компании и доказал свою компетентность и профессионализм.\n'
                           'Ты проделал большую работу и наверняка успел накопить много полезных знаний и опыта. \n'
                           'Поделись впечатлениями о первом рабочем году, расскажи о достижениях и успехах, которыми гордишься больше всего. А также поделись идеями, как мы можем сделать нашу совместную работу ещё эффективнее и комфортнее.\n'
                           'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = await ready_kb(employee.telegram_id))
            
            logger.info(f"Опрос через 12 месяцев отправлен сотруднику {employee_id}")
        except Exception as e:
            logger.error(f"Ошибка при отправке опроса через 12 месяцев сотруднику {employee_id}: {e}")            

def schedule_poll(scheduler, employee, days_delta, send_func):
    """Планирует отправку опроса на указанное количество дней после hire_date"""
    try:
        send_date = employee.hire_date + timedelta(days=days_delta)
        send_time = datetime.combine(
            send_date,
            datetime.strptime("10:00", "%H:%M").time()
        ).replace(tzinfo=None)
        
        if send_time > datetime.now():
            scheduler.add_job(
                send_func,
                trigger=DateTrigger(run_date=send_time),
                args=[employee.id],
                id=f"poll_{days_delta}days_{employee.id}",
                replace_existing=True
            )
            logger.info(f"Запланирован опрос через {days_delta} дней для сотрудника {employee.id} на {send_time}")
        else:
            asyncio.create_task(send_func(employee.id))
    except Exception as e:
        logger.error(f"Ошибка при планировании опроса для сотрудника {employee.id}: {e}")


async def log_scheduler_status(scheduler: AsyncIOScheduler):
    """Логирует статус планировщика каждые 5 минут"""
    logger.info(
        f"Scheduler: запущен"
    )

async def schedule_polls():
    """Основная функция планирования опросов"""
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    try:
        #каждые 5 минут проверяем статус
        scheduler.add_job(
        log_scheduler_status,
        'interval',
        minutes=5,
        args=[scheduler],
        id='scheduler',
        replace_existing=True
        )
         
        employees = await sync_to_async(list)(Employee.objects.exclude(hire_date__isnull=True))
        logger.info(f"Найдено {len(employees)} сотрудников для планирования опросов")
        
        for employee in employees:
            if not employee.hire_date:
                continue
            
            try:
                today = datetime.now().date()
                days_employed = (today - employee.hire_date).days
                logger.info(f"Сотрудник {employee.id}, работает {days_employed} дней")
                
                # Для новых сотрудников (<1 месяца) - планируем опросы
                if days_employed < 30:
                    schedule_poll(scheduler, employee, 30, send_poll_after_1_month)
                    schedule_poll(scheduler, employee, 90, send_poll_after_3_month)
                    schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
                    schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
                
                # Для работающих 1-3 месяца
                elif 30 <= days_employed < 90:
                    if await is_user_available(employee.telegram_id):
                        await send_poll_after_1_month(employee.id)
                        schedule_poll(scheduler, employee, 90, send_poll_after_3_month)
                        schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
                        schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
                
                # Для работающих 3-6 месяцев
                elif 90 <= days_employed < 180:
                    if await is_user_available(employee.telegram_id):
                        await send_poll_after_3_month(employee.id)
                        schedule_poll(scheduler, employee, 180, send_poll_after_6_month)
                        schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
                
                # Для работающих >6 месяцев - не отправляем
                else:
                    await send_poll_after_6_month(employee.id)
                    schedule_poll(scheduler, employee, 365, send_poll_after_12_month)
            
            except Exception as e:
                logger.error(f"Ошибка обработки сотрудника {employee.id}: {e}")
                continue
        
        scheduler.start()
        logger.info("Планировщик опросов успешно запущен")
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске планировщика: {e}")
        raise

# import asyncio
# from datetime import datetime, timedelta
# from apscheduler.schedulers.asyncio import AsyncIOScheduler
# from apscheduler.triggers.date import DateTrigger
# from create_bot import bot, dp
# from core.models import Employee
# from asgiref.sync import sync_to_async
# from handlers.after_1_month import Form_1
# from handlers.after_3_month import Form_3
# from handlers.after_6_month import Form_6
# from bot.keyboards import ready_kb

# # Отправляет опрос через 1 месяц после трудоустройства
# async def send_poll_after_1_month(employee_id):
#     employee = await sync_to_async(Employee.objects.get)(id = employee_id)
#     state = dp.fsm.get_context(bot = bot, chat_id = employee.telegram_id, user_id = employee.telegram_id)
#     await state.set_state(Form_1.how_are_you)
#     await bot.send_message(
#         chat_id = employee.telegram_id,
#         text = 'Привет!\nПоздравляем с первым месяцем в команде!\n\n'
#         'Чтобы оценить, как идут дела, предлагаем пройти опрос по чек-листу.\n\n'
#         'Готов(а)? Нажимай кнопку «Готов(а)»',
#         reply_markup = ready_kb(employee.telegram_id)
#     )

# # Отправляет опрос через 3 месяца после трудоустройства
# async def send_poll_after_3_month(employee_id):
#     employee = await sync_to_async(Employee.objects.get)(id = employee_id)
#     state = dp.fsm.get_context(bot = bot, chat_id = employee.telegram_id, user_id = employee.telegram_id)
#     await state.set_state(Form_3.how_are_you)
#     await bot.send_message(
#         chat_id = employee.telegram_id,
#         text = 'Привет!\n\n'
#         'Три месяца в компании — отличный результат!\n\n'
#         'Твой адаптационный период подходит к концу, и мне важно узнать, '
#         'как у тебя идут дела. Поделись своими впечатлениями, пожалуйста, '
#         'ответив на предложенные вопросы.\n\n'
#         'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(employee.telegram_id)
#     )

# # Отправляет опрос через 6 месяцев после трудоустройства
# async def send_poll_after_6_month(employee_id):
#     employee = await sync_to_async(Employee.objects.get)(id = employee_id)
#     state = dp.fsm.get_context(bot = bot, chat_id = employee.telegram_id, user_id = employee.telegram_id)
#     await state.set_state(Form_6.how_are_you)
#     await bot.send_message(
#         chat_id = employee.telegram_id,
#         text = 'Привет!\n\n'
#         'Поздравляю с достижением экватора трудового стажа в нашей компании! '
#         'За этот год ты, несомненно, приобрел немало знаний и опыта.\n\n'
#         'Поделишься, как продвигается твоя работа? Ответы на наши вопросы помогут нам лучше понять твою ситуацию.\n\n'
#         'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(employee.telegram_id)
#     )

# # Планирует отправку опроса сотруднику через заданное количество дней
# # Принимает: scheduler - объект планировщика, employee - объект сотрудника, 
# # days_delta - через сколько дней после hire_date отправить опрос, 
# # send_func - функция для отправки опроса
# def schedule_poll(scheduler, employee, days_delta, send_func):
#     send_date = employee.hire_date + timedelta(days = days_delta)
#     send_time = datetime.combine(
#         send_date,
#         datetime.strptime("10:00", "%H:%M").time()
#     ).replace(tzinfo = None)
#     if send_time > datetime.now():
#         scheduler.add_job(
#             send_func,
#             trigger = DateTrigger(run_date = send_time),
#             args = [employee.id],
#             id = f"poll_{days_delta}days_{employee.id}",
#             replace_existing = True
#         )
#     else:
#         asyncio.create_task(send_func(employee.id))

# # Планировщик опросов
# async def schedule_polls():
#     scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
#     try:
#         employees = await sync_to_async(list)(Employee.objects.exclude(hire_date__isnull = True))
#         for employee in employees:
#             if not employee.hire_date:
#                 continue
#             try:
#                 # Опрос через 1 месяц
#                 schedule_poll(schedule = scheduler, employee = employee,
#                               days_delta = 30, send_func = send_poll_after_1_month)
#                 # Опрос через 3 месяца
#                 schedule_poll(scheduler = scheduler, employee = employee,
#                               days_delta = 90, send_func = send_poll_after_3_month)
#                 # Опрос через 6 месяцев
#                 schedule_poll(scheduler = scheduler, employee = employee,
#                               days_delta = 180, send_func = send_poll_after_6_month)
#             except Exception as e:
#                 print(f"Ошибка для сотрудника {employee.id}: {e}")
#                 continue
#         scheduler.start()
#     except Exception as e:
#         print(f"Критическая ошибка: {e}")
#         raise