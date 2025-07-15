import asyncio
from create_bot import bot
from aiogram.filters import Command
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender

question_router = Router()

short_delay = 1

@question_router.message(Command('хочузадатьвопрос')) # обработка команды /хочузадатьвопрос
@question_router.message(F.text == "Хочу задать вопрос")
async def capture_question(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Приветствую тебя, молодой специалист!\n\n"
                             "Возникли вопросы? Оставь их ниже и ожидай ответа.", reply_markup = ReplyKeyboardRemove())
    await state.clear()