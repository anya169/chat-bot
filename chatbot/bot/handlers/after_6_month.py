import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from keyboards import ready_kb, question_kb # клавиатуры

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 15

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

@after_6_month_router.message(Command('after_6_month'))
async def start_poll_after_1_month(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Привет!\n\n'
                             'Поздравляю с достижением экватора трудового стажа в нашей компании! '
                             'За этот год ты, несомненно, приобрел немало знаний и опыта.\n\n'
                             'Поделишься, как продвигается твоя работа? Ответы на наши вопросы помогут нам лучше понять твою ситуацию.\n\n'
                             'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(message.from_user.id))
    await state.set_state(Form_6.how_are_you)

@after_6_month_router.message(F.text == "Готов(а)", Form_6.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Как дела?", reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form_6.question_1)

@after_6_month_router.message(F.text, Form_6.question_1)
async def question_1(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Как часто ты встречаешься со своим руководителем?")
    await state.set_state(Form_6.question_2)

@after_6_month_router.message(F.text, Form_6.question_2)
async def question_2(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Комфортно ли тебе взаимодействовать с руководителем?")
    await state.set_state(Form_6.question_3)

@after_6_month_router.message(F.text, Form_6.question_3)
async def question_3(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Всегда ли руководитель и наставник дают тебе обратные ответы на вопросы?")
    await state.set_state(Form_6.question_4)

@after_6_month_router.message(F.text, Form_6.question_4)
async def question_4(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Удалось ли принять участие в мероприятиях филиала?")
    await state.set_state(Form_6.question_5)

@after_6_month_router.message(F.text, Form_6.question_5)
async def question_5(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Чего тебе не хватает для улучшения реализации трудовой деятельности?")
    await state.set_state(Form_6.question_6)

@after_6_month_router.message(F.text, Form_6.question_6)
async def question_6(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Может есть волнующие моменты, которые тебя беспокоят?")
    await state.set_state(Form_6.result)

@after_6_month_router.message(F.text, Form_6.result)
async def result(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Мы стремимся к постоянному развитию наших сотрудников и предлагаем тебе пройти "
                             "тестирование для самоанализа личного профиля.\n\n"
                             "Для прохождения теста перейди по ссылке: [ссылка].\n\n"
                             "Итоги самооценки будут предоставлены в виде отчета, который направит куратор.\n\n"
                             "Благодарим за сотрудничество! До встречи!", reply_markup = question_kb(message.from_user.id))
    await state.clear()