import asyncio
from bot.create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from bot.keyboards import ready_kb, question_kb # клавиатуры
from datetime import date, timedelta
import os
import django
import sys
from asgiref.sync import sync_to_async


from core.models import Employee, Answer

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 1

# состояния бота
class Form_6(StatesGroup):
    how_are_you = State()
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    result = State()
    
after_6_month_router = Router()

# Получает объект сотрудника из базы данных по его telegram id
# Принимает: telegram_id — идентификатор пользователя в telegram
# Возвращает: объект Employee или вызывает исключение, если сотрудник не найден
async def get_employee(telegram_id):
    return await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)

# Сохраняет ответ сотрудника в базу данных
# Принимает: employee — сотрудник, ответивший на вопрос, message_text — текст ответа, question_id — id вопроса в базе данных
async def save_answer(employee, message_text, question_id):
    today = date.today()
    delta = today - employee.hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name = message_text,
        login_id = employee.id,
        question_id = question_id - 1
    )
    await sync_to_async(employee_answer.save)()

# Обрабатывает ответ на вопрос, сохраняет его и задает следующий вопрос
# Принимает: message — сообщение от пользователя, state — текущее состояние диалога, next_state — следующее состояние или None для завершения,
# question_text — текст следующего вопроса, question_id — id следующего вопроса в базе данных, reply_markup (опционально) — клавиатура для ответа
async def handle_question(message: Message, state: FSMContext, next_state, question_text, question_id, reply_markup = None):
    telegram_id = message.from_user.id
    employee = await get_employee(telegram_id)
    await save_answer(employee, message.text, question_id)
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(question_text, reply_markup = reply_markup)
    if next_state:
        await state.set_state(next_state)

# Завершает опрос, сохраняет последний ответ (если нужно) и отправляет благодарность
# Принимает: message — последнее сообщение от пользователя, state — текущее состояние диалога, question_id (int, опционально) — id вопроса, если последний ответ нужно сохранить
async def finish_poll(message: Message, state: FSMContext, question_id = None):
    if question_id:
        telegram_id = message.from_user.id
        employee = await get_employee(telegram_id)
        await save_answer(employee, message.text, question_id)
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Мы стремимся к постоянному развитию наших сотрудников и предлагаем тебе пройти "
            "тестирование для самоанализа личного профиля.\n\n"
            "Для прохождения теста перейди по ссылке: https://forms.yandex.ru/u/666affe3c417f301ddc2a6a9 .\n\n"
            "Итоги самооценки будут предоставлены в виде отчета, который я направлю тебе по итогам обработки 👌\n\n"
            "Благодарю за сотрудничество! До встречи!"
        )
    await state.clear()

@after_6_month_router.message(Command('after_6_month'))
async def start_poll_after_1_month(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Привет!\n\n'
                             'Поздравляю с успешным завершением первого трудового года в нашем дружном коллективе! ✨'
                             'Прошедший год показал, насколько значима твоя роль в команде. Ты активно участвовал в развитии компании, проявил высокий уровень профессионализма и компетенции.\n\n'
                             'Предлагаю поделиться своими ощущениями и эмоциями от первого рабочего года? Рассказать о главных профессиональных достижениях, которыми особенно гордишься и помнишь. И конечно же, предложи свои идеи, как нам сделать сотрудничество еще продуктивнее и приятнее! 🙂\n\n'
                             'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = await ready_kb(message.from_user.id))
    await state.set_state(Form_6.how_are_you)

@after_6_month_router.message(F.text == "Готов(а)", Form_6.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Как обстоят дела в производственной среде?",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(Form_6.question_1)

@after_6_month_router.message(F.text, Form_6.question_1)
async def question_1(message: Message, state: FSMContext):
    await handle_question(message, state, Form_6.question_2, "Как часто ты встречаешься со своим руководителем?", 32)

@after_6_month_router.message(F.text, Form_6.question_2)
async def question_2(message: Message, state: FSMContext):
    await handle_question(message, state, Form_6.question_3, "Комфортно ли тебе взаимодействовать с руководителем?", 33)

@after_6_month_router.message(F.text, Form_6.question_3)
async def question_3(message: Message, state: FSMContext):
    await handle_question(message, state, Form_6.question_4, "Всегда ли руководитель и наставник дают тебе обратные ответы на вопросы?", 34)

@after_6_month_router.message(F.text, Form_6.question_4)
async def question_4(message: Message, state: FSMContext):
    await handle_question(message, state, Form_6.question_5, "Удалось ли принять участие в мероприятиях филиала?", 35)

@after_6_month_router.message(F.text, Form_6.question_5)
async def question_5(message: Message, state: FSMContext):
    await handle_question(message, state, Form_6.question_6, "Чего тебе не хватает для улучшения реализации трудовой деятельности?", 36)

@after_6_month_router.message(F.text, Form_6.question_6)
async def question_6(message: Message, state: FSMContext):
    await handle_question(message, state, Form_6.result, "Может есть волнующие моменты, которые тебя беспокоят?", 37)

@after_6_month_router.message(F.text, Form_6.result)
async def result(message: Message, state: FSMContext):
    await finish_poll(message, state, 38)