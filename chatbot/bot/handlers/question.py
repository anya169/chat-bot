import asyncio
from create_bot import bot
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from aiogram.filters.state import State, StatesGroup
import os
import django
import sys
from asgiref.sync import sync_to_async

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
from core.models import Employee, Special_Question

class Form_question(StatesGroup):
    question = State()

question_router = Router()

short_delay = 1

@question_router.message(Command('хочузадатьвопрос')) # обработка команды /хочузадатьвопрос
@question_router.message(F.text == "Хочу задать вопрос")
async def capture_question(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Приветствую тебя, молодой специалист!\n\n"
                             "Возникли вопросы? Оставь их ниже и ожидай ответа.", reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form_question.question)

@question_router.message(F.text, Form_question.question)
async def capture_name(message: Message, state: FSMContext):
    question = message.text
    telegram_id = message.from_user.id 
    try:
        employee = await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)
        special_question = Special_Question(
            name = question,
            employee_id_id = employee.id 
        )
        await sync_to_async(special_question.save)()
        await asyncio.sleep(short_delay)
        await message.answer("Ваш вопрос сохранен! Ожидайте ответа.")
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        await asyncio.sleep(short_delay)
        await message.answer('Произошла ошибка при сохранении ваших данных. Пожалуйста, попробуйте позже.')
    await state.clear()