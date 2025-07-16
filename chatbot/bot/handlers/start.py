from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards import tell_about_myself_kb # клавиатура

start_router = Router()

@start_router.message(CommandStart()) # обработка команды /start
async def cmd_start(message: Message):
    await message.answer('Приветствую тебя, молодой специалист!\n\n'
                         'Я твой личный цифровой помощник, который будет сопровождать тебя на пути профессионального роста. '
                         'Вместе мы найдем ответы на все интересующие тебя вопросы.\n\n'
                         'Но для начала давай знакомиться!\n'
                         'Расскажи о себе, отвечая на вопросы, для этого нажми на кнопку \"Рассказать о себе\".',
                         reply_markup = tell_about_myself_kb(message.from_user.id))