import asyncio
from datetime import datetime, timedelta
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.date import DateTrigger
from create_bot import bot, dp
from core.models import Employee
from asgiref.sync import sync_to_async
from handlers.after_1_month import Form_1
from handlers.after_3_month import Form_3
from handlers.after_6_month import Form_6
from bot.keyboards import ready_kb

# Отправляет опрос через 1 месяц после трудоустройства
async def send_poll_after_1_month(employee_id):
    employee = await sync_to_async(Employee.objects.get)(id = employee_id)
    state = dp.fsm.get_context(bot = bot, chat_id = employee.telegram_id, user_id = employee.telegram_id)
    await state.set_state(Form_1.how_are_you)
    await bot.send_message(
        chat_id = employee.telegram_id,
        text = 'Привет!\nПоздравляем с первым месяцем в команде!\n\n'
        'Чтобы оценить, как идут дела, предлагаем пройти опрос по чек-листу.\n\n'
        'Готов(а)? Нажимай кнопку «Готов(а)»',
        reply_markup = ready_kb(employee.telegram_id)
    )

# Отправляет опрос через 3 месяца после трудоустройства
async def send_poll_after_3_month(employee_id):
    employee = await sync_to_async(Employee.objects.get)(id = employee_id)
    state = dp.fsm.get_context(bot = bot, chat_id = employee.telegram_id, user_id = employee.telegram_id)
    await state.set_state(Form_3.how_are_you)
    await bot.send_message(
        chat_id = employee.telegram_id,
        text = 'Привет!\n\n'
        'Три месяца в компании — отличный результат!\n\n'
        'Твой адаптационный период подходит к концу, и мне важно узнать, '
        'как у тебя идут дела. Поделись своими впечатлениями, пожалуйста, '
        'ответив на предложенные вопросы.\n\n'
        'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(employee.telegram_id)
    )

# Отправляет опрос через 6 месяцев после трудоустройства
async def send_poll_after_6_month(employee_id):
    employee = await sync_to_async(Employee.objects.get)(id = employee_id)
    state = dp.fsm.get_context(bot = bot, chat_id = employee.telegram_id, user_id = employee.telegram_id)
    await state.set_state(Form_6.how_are_you)
    await bot.send_message(
        chat_id = employee.telegram_id,
        text = 'Привет!\n\n'
        'Поздравляю с достижением экватора трудового стажа в нашей компании! '
        'За этот год ты, несомненно, приобрел немало знаний и опыта.\n\n'
        'Поделишься, как продвигается твоя работа? Ответы на наши вопросы помогут нам лучше понять твою ситуацию.\n\n'
        'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(employee.telegram_id)
    )

# Планирует отправку опроса сотруднику через заданное количество дней
# Принимает: scheduler - объект планировщика, employee - объект сотрудника, 
# days_delta - через сколько дней после hire_date отправить опрос, 
# send_func - функция для отправки опроса
def schedule_poll(scheduler, employee, days_delta, send_func):
    send_date = employee.hire_date + timedelta(days = days_delta)
    send_time = datetime.combine(
        send_date,
        datetime.strptime("10:00", "%H:%M").time()
    ).replace(tzinfo = None)
    if send_time > datetime.now():
        scheduler.add_job(
            send_func,
            trigger = DateTrigger(run_date = send_time),
            args = [employee.id],
            id = f"poll_{days_delta}days_{employee.id}",
            replace_existing = True
        )
    else:
        asyncio.create_task(send_func(employee.id))

# Планировщик опросов
async def schedule_polls():
    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    try:
        employees = await sync_to_async(list)(Employee.objects.exclude(hire_date__isnull = True))
        for employee in employees:
            if not employee.hire_date:
                continue
            try:
                # Опрос через 1 месяц
                schedule_poll(schedule = scheduler, employee = employee,
                              days_delta = 30, send_func = send_poll_after_1_month)
                # Опрос через 3 месяца
                schedule_poll(scheduler = scheduler, employee = employee,
                              days_delta = 90, send_func = send_poll_after_3_month)
                # Опрос через 6 месяцев
                schedule_poll(scheduler = scheduler, employee = employee,
                              days_delta = 180, send_func = send_poll_after_6_month)
            except Exception as e:
                print(f"Ошибка для сотрудника {employee.id}: {e}")
                continue
        scheduler.start()
    except Exception as e:
        print(f"Критическая ошибка: {e}")
        raise