import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from datetime import date, timedelta
from keyboards import ready_kb, question_kb # клавиатуры
import os
import django
import sys
from asgiref.sync import sync_to_async

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
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

@after_3_month_router.message(Command('after_3_month'))
async def start_poll_after_1_month(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Привет!\n\n'
                             'Три месяца в компании — отличный результат!\n\n'
                             'Твой адаптационный период подходит к концу, и мне важно узнать, '
                             'как у тебя идут дела. Поделись своими впечатлениями, пожалуйста, '
                             'ответив на предложенные вопросы.\n\n'
                             'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(message.from_user.id))
    await state.set_state(Form_3.how_are_you)

@after_3_month_router.message(F.text == "Готов(а)", Form_3.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Как дела?", reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form_3.question_1)

@after_3_month_router.message(F.text, Form_3.question_1)
async def question_1(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 19
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Как часто ты встречаешься со своим руководителем?")
    await state.set_state(Form_3.question_2)

@after_3_month_router.message(F.text, Form_3.question_2)
async def question_2(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 20
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Комфортно ли тебе взаимодействовать с руководителем?")
    await state.set_state(Form_3.question_3)

@after_3_month_router.message(F.text, Form_3.question_3)
async def question_3(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 21
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("В каком формате ты получаешь задачи?")
    await state.set_state(Form_3.question_4)

@after_3_month_router.message(F.text, Form_3.question_4)
async def question_4(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 22
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Дают ли тебе обратную связь?")
    await state.set_state(Form_3.question_5)

@after_3_month_router.message(F.text, Form_3.question_5)
async def question_5(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 23
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Как часто ее дает тебе руководитель?\n"
                             "А наставник?")
    await state.set_state(Form_3.question_6)

@after_3_month_router.message(F.text, Form_3.question_6)
async def question_6(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 24
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Положительная или отрицательная обратная связь?")
    await state.set_state(Form_3.question_7)

@after_3_month_router.message(F.text, Form_3.question_7)
async def question_7(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 25
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Всегда ли руководитель и наставник дают тебе обратные ответы на вопросы?")
    await state.set_state(Form_3.question_8)

@after_3_month_router.message(F.text, Form_3.question_8)
async def question_8(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 26
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Полезен ли закрепленный за тобой наставник?")
    await state.set_state(Form_3.question_9)

@after_3_month_router.message(F.text, Form_3.question_9)
async def question_9(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 27
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Удалось ли принять участие в мероприятиях филиала?")
    await state.set_state(Form_3.question_10)

@after_3_month_router.message(F.text, Form_3.question_10)
async def question_10(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 28
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Чего тебе не хватает для улучшения реализации трудовой деятельности?")
    await state.set_state(Form_3.question_11)

@after_3_month_router.message(F.text, Form_3.question_11)
async def question_11(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 29
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Может есть волнующие моменты, которые тебя беспокоят?")
    await state.set_state(Form_3.result)

@after_3_month_router.message(F.text, Form_3.result)
async def result(message: Message, state: FSMContext):
    telegram_id = message.from_user.id
    employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
    today = date.today()
    hire_date = employee.hire_date
    delta = today - hire_date
    days_passed = delta.days
    employee_answer = Answer(
        name =  message.text,
        submission_date = timedelta(days = days_passed),
        login_id = employee.id,
        question_id = 30
    )
    await sync_to_async(employee_answer.save)()
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Спасибо за предоставленную информацию!\n"
                             "Куратор изучит ответы и, если потребуется, свяжется с тобой!", 
                             reply_markup = question_kb(message.from_user.id))
    await state.clear()