import asyncio
import websockets
import json
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

WEBSOCKET_URL = "ws://localhost:8000/ws/chat/"
active_websockets = {}

async def get_websocket_connection(employee_id):
    if employee_id in active_websockets:
        ws = active_websockets[employee_id]
        if not ws.closed:
            return ws
    
    try:
        ws = await websockets.connect(
            f"{WEBSOCKET_URL}{employee_id}/",
            ping_interval=20,
            close_timeout=10
        )
        active_websockets[employee_id] = ws
        return ws
    except Exception as e:
        print(f"Ошибка подключения WebSocket: {e}")
        return None

async def send_via_websocket(employee_id, message_text, sender_id):
    """Отправка сообщения через WebSocket """
    try:
        ws = await get_websocket_connection(employee_id)
        if ws:
            await ws.send(json.dumps({
                "message": message_text,
                "sender_id": sender_id  
            }))
            print(f"Сообщение отправлено через WebSocket: {message_text}")
    except Exception as e:
        print(f"Ошибка WebSocket: {e}")
        # Удаляем нерабочее соединение
        if employee_id in active_websockets:
            del active_websockets[employee_id]
        raise

@question_router.message(Command('askquestion'))
@question_router.message(F.text == "Хочу задать вопрос")
async def capture_question(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Приветствую тебя, молодой специалист!\n\n"
            "Возникли вопросы? Оставь их ниже и ожидай ответа. Если у тебя несколько вопросов, напиши их в одном сообщении.",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(Form_question.question)

@question_router.message(F.text, Form_question.question)
async def process_question(message: Message, state: FSMContext):
    question = message.text
    telegram_id = message.from_user.id
    
    try:
        # Получаем данные сотрудника
        employee = await sync_to_async(Employee.objects.get)(telegram_id=telegram_id)
        
        # Сохраняем вопрос в базу
        special_question = Special_Question(
            name=question,
            employee_id=employee.id,
        )
        await sync_to_async(special_question.save)()
        
        # Отправляем через WebSocket
        await send_via_websocket(
            employee_id=employee.id,
            message_text=question,
            sender_id=employee.login
        )
        
        await asyncio.sleep(short_delay)
        await message.answer("Спасибо за вопрос! Скоро вернусь с ответом от куратора.")
        
    except Employee.DoesNotExist:
        await message.answer("Ошибка: ваш профиль сотрудника не найден.")
    except Exception as e:
        print(f"Ошибка при обработке вопроса: {e}")
        await message.answer('Произошла ошибка. Пожалуйста, попробуйте позже.')
    
    await state.clear()
    
async def close_all_websockets():
    """Закрывает все WebSocket соединения при завершении"""
    for ws in active_websockets.values():
        if not ws.closed:
            await ws.close()
    active_websockets.clear()

# Регистрируем обработчик закрытия
import atexit
atexit.register(lambda: asyncio.run(close_all_websockets()))

@question_router.message(F.text == "Вопросов нет")
async def capture_question(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Отлично, раз вопросов нет, желаю тебе отличной работы!"
        )
    await state.clear()