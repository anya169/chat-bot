import asyncio
from bot.create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from datetime import date, timedelta
from bot.keyboards import ready_kb, question_kb # клавиатуры
import os
import django
import sys
from asgiref.sync import sync_to_async

from core.models import Employee, Answer

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 1

# состояния бота
class Form_3(StatesGroup):
    how_are_you = State()
    question_1 = State()
    question_2 = State()
    question_3 = State()
    question_4 = State()
    question_5 = State()
    question_6 = State()
    question_7 = State()
    question_8 = State()
    question_9 = State()
    question_10 = State()
    question_11 = State()
    result = State()
    
after_3_month_router = Router()

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
async def finish_poll(message: Message, state: FSMContext, question_id=None):
    if question_id:
        telegram_id = message.from_user.id
        employee = await get_employee(telegram_id)
        await save_answer(employee, message.text, question_id)
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Спасибо за предоставленную информацию!\n"
            "Ответы будут внимательно рассмотрены куратором, и при необходимости он обязательно свяжется с тобой дополнительно. До связи! 💬",
            reply_markup = await question_kb(message.from_user.id)
        )
    await state.clear()

@after_3_month_router.message(Command('after_3_month'))
async def start_poll_after_3_month(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Привет!\n\n'
                             'Три месяца в компании — отличный результат!\n\n'
                             'Первая ступень твоего адаптационного периода подходит к концу, и мне важно узнать, '
                             'как у тебя идут дела. Поделись своими впечатлениями, пожалуйста, '
                             'ответив на предложенные вопросы.\n\n'
                             'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = await ready_kb(message.from_user.id))
    await state.set_state(Form_3.how_are_you)

@after_3_month_router.message(F.text == "Готов(а)", Form_3.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Как обстоят дела в производственной среде?",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(Form_3.question_1)

@after_3_month_router.message(F.text, Form_3.question_1)
async def question_1(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_2, "Как часто ты встречаешься со своим руководителем?", 20)

@after_3_month_router.message(F.text, Form_3.question_2)
async def question_2(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_3, "Комфортно ли тебе взаимодействовать с руководителем?", 21)

@after_3_month_router.message(F.text, Form_3.question_3)
async def question_3(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_4, "В каком формате ты получаешь задачи?", 22)

@after_3_month_router.message(F.text, Form_3.question_4)
async def question_4(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_5, "Дают ли тебе обратную связь?", 23)

@after_3_month_router.message(F.text, Form_3.question_5)
async def question_5(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_6, "Как часто ее дает тебе руководитель?\nА наставник?", 24)

@after_3_month_router.message(F.text, Form_3.question_6)
async def question_6(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_7, "Положительная или отрицательная обратная связь?", 25)

@after_3_month_router.message(F.text, Form_3.question_7)
async def question_7(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_8, "Всегда ли руководитель и наставник дают тебе обратные ответы на вопросы?", 26)

@after_3_month_router.message(F.text, Form_3.question_8)
async def question_8(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_9, "Полезен ли закрепленный за тобой наставник?", 27)

@after_3_month_router.message(F.text, Form_3.question_9)
async def question_9(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_10, "Удалось ли принять участие в мероприятиях филиала?", 28)

@after_3_month_router.message(F.text, Form_3.question_10)
async def question_10(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.question_11, "Чего тебе не хватает для улучшения реализации трудовой деятельности?", 29)

@after_3_month_router.message(F.text, Form_3.question_11)
async def question_11(message: Message, state: FSMContext):
    await handle_question(message, state, Form_3.result, "Может есть волнующие моменты, которые тебя беспокоят?", 30)

@after_3_month_router.message(F.text, Form_3.result)
async def result(message: Message, state: FSMContext):
    await finish_poll(message, state, 31)