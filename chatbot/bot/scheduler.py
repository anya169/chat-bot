import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
from apscheduler.triggers.date import DateTrigger
import sys
from django.conf import settings
from .create_bot import bot, dp 
from core.models import *
from asgiref.sync import sync_to_async
from bot.handlers.after_1_month import Form_1
from bot.handlers.after_3_month import Form_3
from bot.handlers.after_6_month import Form_6
from bot.handlers.after_12_month import Form_12
from bot.handlers.after_18_month import Form_18
from bot.handlers.after_24_month import Form_24
from bot.handlers.after_30_month import Form_30
from bot.handlers.after_36_month import Form_36
from bot.handlers.after_14_days import Form_14
from bot.keyboards import ready_kb
import logging
from channels.db import database_sync_to_async

_scheduler_instance = None

def get_scheduler():
    """Возвращает глобальный экземпляр планировщика"""
    global _scheduler_instance
    logger.info(f"📋 get_scheduler() возвращает: {_scheduler_instance}")
    if _scheduler_instance:
        logger.info(f"⚡ Планировщик running: {_scheduler_instance.running}")
    return _scheduler_instance

async def has_completed_poll(employee_id, poll_name):
    try:
        poll = await sync_to_async(Poll.objects.get, thread_sensitive=True)(name=poll_name)
        queryset = Answer.objects.filter(login_id=employee_id, question__poll=poll)
        exists = await sync_to_async(queryset.exists, thread_sensitive=True)()
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
        return True

async def send_poll_after_14_days(employee_id):
    if (not await has_completed_poll(employee_id, "Опрос через 14 дней")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 14 дней отложен")
                return
            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_14.question_1)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Приветствую тебя, молодой специалист! 👋\n\n'
                           'Это я – Газоптикум, твой личный цифровой помощник! \n'
                           'Расскажи, как проходят первые рабочие дни?\n'
                           'Отметь в опросе ниже ⬇')
            
            await bot.send_poll(
                chat_id=employee.telegram_id,
                question="Как у тебя дела?",
                options=["Все отлично! 👍", "Все хорошо! 😊", "Средне", "Хотелось бы, чтоб было лучше …🙁", "Все плохо! 😢"],
                is_anonymous=False,
                allows_multiple_answers=False,
                type="regular"
            )              
            await state.update_data(poll_options=["Все отлично! 👍", "Все хорошо! 😊", "Средне", "Хотелось бы, чтоб было лучше …🙁", "Все плохо! 😢"])
            await bot.send_message(
                chat_id=employee.telegram_id,
                text="Как обстоят дела с организацией твоей производственной деятельности? Возможно что-то идет не так, как хотелось бы? Опиши в нескольких предложениях ⬇"
            )
            await state.set_state(Form_14.question_3)
            logger.info(f"Опрос через 14 дней отправлен сотруднику {employee_id}")

        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 14 дней сотруднику {employee_id}: {e}")

async def send_poll_after_1_month(employee_id):
    if (not await has_completed_poll(employee_id, "Опрос через месяц")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
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
                text='Привет!\nПоздравляю тебя с успешным стартом в нашей команде — прошёл уже целый месяц! 😊\n\n'
                    'Для того, чтобы мы могли вместе увидеть, насколько успешно идёт процесс адаптации, предлагаю заполнить небольшой опрос по чек-листу обратной связи.\n\n'
                    'Готов(а)? Нажимай кнопку «Готов(а)»',
                reply_markup=await ready_kb(employee.telegram_id)
            )
            
            logger.info(f"Опрос через 1 месяц отправлен сотруднику {employee_id}")

        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 1 месяц сотруднику {employee_id}: {e}")

async def send_poll_after_3_month(employee_id):
    """Отправляет опрос через 3 месяца после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 3 месяца")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
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
                    'Первая ступень твоего адаптационного периода подходит к концу, и мне важно узнать, '
                    'как у тебя идут дела. Поделись своими впечатлениями, пожалуйста, '
                    'ответив на предложенные вопросы.\n\n'
                    'Готов(а)? Нажимай кнопку «Готов(а)»',
                reply_markup=await ready_kb(employee.telegram_id)
            )
            logger.info(f"Опрос через 3 месяца отправлен сотруднику {employee_id}")
        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 3 месяца сотруднику {employee_id}: {e}")

async def send_poll_after_6_month(employee_id):
    """Отправляет опрос через 6 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 6 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
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
                    'Поздравляю с успешным завершением первого трудового года в нашем дружном коллективе! ✨'
                    'Прошедший год показал, насколько значима твоя роль в команде. Ты активно участвовал в развитии компании, проявил высокий уровень профессионализма и компетенции.\n\n'
                    'Предлагаю поделиться своими ощущениями и эмоциями от первого рабочего года? Рассказать о главных профессиональных достижениях, которыми особенно гордишься и помнишь. И конечно же, предложи свои идеи, как нам сделать сотрудничество еще продуктивнее и приятнее! 🙂\n\n'
                    'Готов(а)? Нажимай кнопку «Готов(а)»',
                reply_markup=await ready_kb(employee.telegram_id)
            )
            logger.info(f"Опрос через 6 месяцев отправлен сотруднику {employee_id}")
        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 6 месяцев сотруднику {employee_id}: {e}")
            
async def send_poll_after_12_month(employee_id):
    """Отправляет опрос через 12 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 12 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
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
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 12 месяцев сотруднику {employee_id}: {e}")            

async def send_poll_after_18_month(employee_id):
    """Отправляет опрос через 18 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 18 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 18 месяцев отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_18.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                           'Поздравляю с прохождением половины пути в качестве молодого специалиста нашей команды! 🚀 \n\n'
                           'Позади уже немало ценной практики, впереди ждут новые горизонты и профессиональные вершины! \n'
                           'Поделись своим мнением о сегодняшних рабочих процессах и предложи идеи, как сделать твою работу еще интересней и продуктивней.\n'
                           'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = await ready_kb(employee.telegram_id))
            
            logger.info(f"Опрос через 18 месяцев отправлен сотруднику {employee_id}")
        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 18 месяцев сотруднику {employee_id}: {e}")            

async def send_poll_after_24_month(employee_id):
    """Отправляет опрос через 24 месяца после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 24 месяца")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 24 месяца отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_24.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                           'Поздравляю с двухлетием в нашей команде! 🎯\n\n'
                           'Прошло уже целых два года — ты прошёл огромный путь, доказал свою преданность профессии и сделал значительный вклад в развитие компании. Впереди ждут новые рубежи и захватывающие испытания!\n'
                           'Поделись мыслями о нынешней работе, расскажи, как видишь своё дальнейшее развитие и как можно сделать рабочие процессы ещё более интересными и эффективными.\n'
                           'Готов(а) к обсуждению и новому этапу развития? Жми кнопку «Готов(а)»!', reply_markup = await ready_kb(employee.telegram_id))
            
            logger.info(f"Опрос через 24 месяца отправлен сотруднику {employee_id}")
        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 24 месяца сотруднику {employee_id}: {e}")            

async def send_poll_after_30_month(employee_id):
    """Отправляет опрос через 30 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 30 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 30 месяцев отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_30.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                           'Поздравляю с преодолением важной отметки — 2,5 года работы в нашем дружном коллективе! 🌟\n\n'
                           'Уже многое успел, впереди — ещё больше интересного. Расскажи, как тебе работается сейчас и какие идеи есть для улучшений.\n\n'
                           'Готов(а)?', reply_markup = await ready_kb(employee.telegram_id))
            
            logger.info(f"Опрос через 30 месяцев отправлен сотруднику {employee_id}")
        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 30 месяцев сотруднику {employee_id}: {e}")            

async def send_poll_after_36_month(employee_id):
    """Отправляет опрос через 36 месяцев после трудоустройства"""
    if (not await has_completed_poll(employee_id, "Опрос через 36 месяцев")): #если сотрудник еще не проходил опрос
        try:
            employee = await sync_to_async(Employee.objects.get, thread_sensitive=True)(id=employee_id)
            if not await is_user_available(employee.telegram_id):
                logger.info(f"Пользователь {employee.telegram_id} занят, опрос через 36 месяцев отложен")
                return

            state = dp.fsm.get_context(
                bot=bot,
                chat_id=employee.telegram_id,
                user_id=employee.telegram_id
            )
            await state.set_state(Form_36.how_are_you)
            
            await bot.send_message(
                chat_id=employee.telegram_id,
                text='Привет!\n\n'
                         'Поздравляю с успешными тремя годами работы в нашей команде! 🎉\n\n'
                           'Уверен, что успехов достигнуто не мало!\n'
                           'Но сегодня отличный повод вспомнить пройденный путь и обсудить дальнейшие планы.\n'
                           'Давай поговорим о том, как тебе работается сейчас, какие успехи достиг, и какие предложения у тебя есть для повышения эффективности и интереса в твоей работе!\n'
                           'Что скажешь? Нажми «Готов»!', reply_markup = await ready_kb(employee.telegram_id))
            
            logger.info(f"Опрос через 36 месяцев отправлен сотруднику {employee_id}")
        except Exception as e:
            from bot.config import add_to_blocked
            add_to_blocked(employee.telegram_id)
            logger.error(f"Ошибка при отправке опроса через 36 месяцев сотруднику {employee_id}: {e}")            



def schedule_poll_hire(scheduler, employee, days_delta, send_func):
    """Планирует отправку опроса на указанное количество дней после hire_date"""
    try:
        send_date = employee.hire_date + timedelta(days=days_delta)
        send_time = datetime.combine(
            send_date,
            datetime.strptime("10:00", "%H:%M").time()
        )
        logger.info(f"Время отправки для {employee.id}: {send_time}")

        
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
            scheduler.add_job(
                send_func,
                trigger=DateTrigger(run_date=datetime.now()),
                args=[employee.id],
                id=f"poll_immediate_{employee.id}",
                replace_existing=True
            )
            logger.info(f"Отправлен немедленный опрос для сотрудника {employee.id}")
    except Exception as e:
        logger.error(f"Ошибка при планировании опроса для сотрудника {employee.id}: {e}")

def schedule_poll_tg(scheduler, employee, days_delta, send_func):
    """Планирует отправку опроса на указанное количество дней после регистрации в боте"""
    try:
        send_date = employee.telegram_registration_date + timedelta(days=days_delta)
        send_time = datetime.combine(
            send_date,
            datetime.strptime("10:00", "%H:%M").time()
        )
        logger.info(f"Время отправки для {employee.id}: {send_time}")

        
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
            scheduler.add_job(
                send_func,
                trigger=DateTrigger(run_date=datetime.now()),
                args=[employee.id],
                id=f"poll_immediate_{employee.id}_{days_delta}_days",
                replace_existing=True
            )
            logger.info(f"Отправлен немедленный опрос для сотрудника {employee.id}")
    except Exception as e:
        logger.error(f"Ошибка при планировании опроса для сотрудника {employee.id}: {e}")

def schedule_weekly_polls(scheduler, employee, start_date, times, num, send_func):
    """Планирует опросы с интервалом в неделю начиная с start_date"""
    try:
        for week_number in range(1, times + 1):  # количество недель
            send_date = start_date + timedelta(weeks=(week_number - 1)*num)
            #получаем, в какой день недели расчитана дата отправки
            day_of_week = send_date.weekday()
            #если это понедельник - четверг, то прибавляем дни до пятницы
            if  0 <= day_of_week <= 3:
                send_date += timedelta(days = 4 - day_of_week)
            #если это суббота - воскресенье, то вычитаем дни до пятницы    
            elif  5 <= day_of_week <= 6:
                send_date -= timedelta(days = day_of_week - 4)    
            send_time = datetime.combine(
                send_date,
                datetime.strptime("10:00", "%H:%M").time()
            )
            
            if send_time > datetime.now():
                scheduler.add_job(
                    send_func,
                    trigger=DateTrigger(run_date=send_time),
                    args=[employee.id],
                    id=f"poll_14days_week{week_number}_{employee.id}",
                    replace_existing=True
                )
                logger.info(f"Запланирован опрос неделя {week_number} для сотрудника {employee.id} на {send_time}")
                
    except Exception as e:
        logger.error(f"Ошибка при планировании недельных опросов для сотрудника {employee.id}: {e}")

def log_scheduler_status():
    """Логирует статус планировщика каждые 5 минут"""
    logger.info(
        f"Scheduler: запущен"
    )
    global _scheduler_instance
    asyncio.run(create_all_jobs(_scheduler_instance))

async def schedule_polls():
    """Основная функция планирования опросов"""
    global _scheduler_instance
    db_settings = settings.DATABASES['default']
    if _scheduler_instance and _scheduler_instance.running:
        logger.info("Планировщик уже запущен")
        return _scheduler_instance
    
    # Формируем URL для подключения к PostgreSQL
    db_url = f"postgresql://{db_settings['USER']}:{db_settings['PASSWORD']}@{db_settings['HOST']}:{db_settings['PORT']}/{db_settings['NAME']}"
    
    jobstores = {
        'default': SQLAlchemyJobStore(url=db_url)
    }
    
    executors = {
        'default': ThreadPoolExecutor(3)
    }
    
    job_defaults = {
        'coalesce': True,  #объединять повторные запуски
        'max_instances': 3,
        'misfire_grace_time': 3600  
    }
    
    scheduler = AsyncIOScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults,
        timezone="Europe/Moscow"
    )
    try:
        
        scheduler.start()
        _scheduler_instance = scheduler
        #проверяем есть ли задачи
        existing_jobs = scheduler.get_jobs()
        logger.info(f"Найдено {len(existing_jobs)} существующих задач в хранилище")
        
        #создаем новые задачи только если хранилище пустое
        if not existing_jobs:
            logger.info("Хранилище задач пустое, создаем новые задачи...")
            await create_all_jobs(scheduler)

        
        #каждые 5 минут проверяем статус
        scheduler.add_job(
        log_scheduler_status,
        'interval',
        minutes=5,
        id='scheduler',
        replace_existing=True
        )
         
        logger.info("Планировщик опросов успешно запущен")
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске планировщика: {e}")
        raise

async def create_all_jobs(scheduler):
    employees = await sync_to_async(
        lambda: list(Employee.objects.exclude(hire_date__isnull=True)),
        thread_sensitive=True
    )()        
    logger.info(f"Найдено {len(employees)} сотрудников для планирования опросов")
    
    for employee in employees:
        if not employee.hire_date:
            continue
        
        try:
            today = datetime.now().date()
            days_employed = (today - employee.hire_date).days
            logger.info(f"Сотрудник {employee.id}, работает {days_employed} дней")
            
            # Рассчитываем дату начала недельных опросов: hire_date + кол-во месяцев + недели
            start_weekly_polls_date_from_1_to_3 = employee.hire_date + timedelta(days=44)  # 30 дней + 14 дней
            start_weekly_polls_date_from_3_to_6 = employee.hire_date + timedelta(days=121)  # 90 дней + 21 день
            start_weekly_polls_date_from_6_to_12 = employee.hire_date + timedelta(days=210)  # 180 дней + 30 дней
            start_weekly_polls_date_from_12_to_18 = employee.hire_date + timedelta(days=395)  #365 дней + 30 дней
            start_weekly_polls_date_from_18_to_24 = employee.hire_date + timedelta(days=575)  #545 дней + 30 дней
            start_weekly_polls_date_from_24_to_30 = employee.hire_date + timedelta(days=760)  #730 дней + 30 дней
            start_weekly_polls_date_from_30_to_36 = employee.hire_date + timedelta(days=940)  #910 дней + 30 дней
            
            
            # Для новых сотрудников (<1 месяца) - планируем опросы
            if days_employed <= 30:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 30, send_poll_after_1_month)
                    schedule_poll_hire(scheduler, employee, 90, send_poll_after_3_month)
                    schedule_poll_hire(scheduler, employee, 180, send_poll_after_6_month)
                    schedule_poll_hire(scheduler, employee, 365, send_poll_after_12_month)
                    schedule_poll_hire(scheduler, employee, 545, send_poll_after_18_month)
                    schedule_poll_hire(scheduler, employee, 730, send_poll_after_24_month)
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_1_to_3, 3, 2, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_3_to_6, 4, 3, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_6_to_12, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_12_to_18, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_18_to_24, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
            
            # Для работающих 1-3 месяца
            elif 30 < days_employed < 90:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 90, send_poll_after_3_month)
                    schedule_poll_hire(scheduler, employee, 180, send_poll_after_6_month)
                    schedule_poll_hire(scheduler, employee, 365, send_poll_after_12_month)
                    schedule_poll_hire(scheduler, employee, 545, send_poll_after_18_month)
                    schedule_poll_hire(scheduler, employee, 730, send_poll_after_24_month)
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_1_to_3, 3, 2, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_3_to_6, 4, 3, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_6_to_12, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_12_to_18, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_18_to_24, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
                    
            # Для работающих 3-6 месяцев
            elif 90 <= days_employed < 180:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 180, send_poll_after_6_month)
                    schedule_poll_hire(scheduler, employee, 365, send_poll_after_12_month)
                    schedule_poll_hire(scheduler, employee, 545, send_poll_after_18_month)
                    schedule_poll_hire(scheduler, employee, 730, send_poll_after_24_month)
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_3_to_6, 4, 3, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_6_to_12, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_12_to_18, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_18_to_24, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
                    
            # Для работающих 6-12 месяцев 
            elif 180 <= days_employed < 365:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 365, send_poll_after_12_month)
                    schedule_poll_hire(scheduler, employee, 545, send_poll_after_18_month)
                    schedule_poll_hire(scheduler, employee, 730, send_poll_after_24_month)
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_6_to_12, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_12_to_18, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_18_to_24, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
                    
            # Для работающих 12-18 месяцев       
            elif 365 <= days_employed < 545:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 545, send_poll_after_18_month)
                    schedule_poll_hire(scheduler, employee, 730, send_poll_after_24_month)
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_12_to_18, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_18_to_24, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
            
            # Для работающих 18-24 месяцев       
            elif 545 <= days_employed < 730:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 730, send_poll_after_24_month)
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_18_to_24, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
            
            # Для работающих 24-30 месяцев       
            elif 730 <= days_employed < 910:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 910, send_poll_after_30_month)
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_24_to_30, 6, 4, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)
            
                # Для работающих 30-36 месяцев       
            elif 910 <= days_employed < 1095:
                if await is_user_available(employee.telegram_id):
                    schedule_poll_hire(scheduler, employee, 1095, send_poll_after_36_month)
                    schedule_poll_tg(scheduler, employee, 14, send_poll_after_14_days)
                    schedule_weekly_polls(scheduler, employee, start_weekly_polls_date_from_30_to_36, 6, 4, send_poll_after_14_days)

        except Exception as e:
            logger.error(f"Ошибка обработки сотрудника {employee.id}: {e}")
            continue
