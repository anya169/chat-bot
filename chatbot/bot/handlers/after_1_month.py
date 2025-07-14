import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from keyboards import ready_kb, yes_or_no_kb, question_kb # клавиатуры

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 15

# состояния бота
class Form_1(StatesGroup):
    how_are_you = State()
    track_passing = State()
    question_1 = State()
    yes_question_2 = State()
    yes_question_3 = State()
    no_question_2 = State()
    no_question_3 = State()
    no_question_4 = State()
    no_question_5 = State()
    no_question_6 = State()
    no_question_7 = State()
    no_question_8 = State()
    no_question_9 = State()
    no_question_10 = State()
    no_question_11 = State()
    no_question_12 = State()
    result = State()
    
after_1_month_router = Router()

@after_1_month_router.message(Command('after_1_month'))
async def start_poll_after_1_month(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Привет!\n'
                             'Поздравляем с первым месяцем в команде!\n\n'
                             'Чтобы оценить, как идут дела, предлагаем пройти опрос по чек-листу.\n\n'
                             'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(message.from_user.id))
    await state.set_state(Form_1.how_are_you)

@after_1_month_router.message(F.text == "Готов(а)", Form_1.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Как дела?", reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form_1.track_passing)

@after_1_month_router.message(F.text, Form_1.track_passing)
async def track_passing(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Прошел(а) ли трек в ГИД?", reply_markup = yes_or_no_kb(message.from_user.id))
    await state.set_state(Form_1.question_1)

@after_1_month_router.message(F.text == "Да", Form_1.question_1)
async def question_1(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Был ли полезным и информативным тебе трек в приложении?", reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form_1.yes_question_2)

@after_1_month_router.message(F.text, Form_1.yes_question_2)
async def yes_question_2(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Расскажи, что больше всего заинтересовало?")
    await state.set_state(Form_1.yes_question_3)

@after_1_month_router.message(F.text, Form_1.yes_question_3)
async def yes_question_3(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Есть ли такая информация, которой не хватило?")
    await state.set_state(Form_1.result)

@after_1_month_router.message(F.text == "Нет", Form_1.question_1)
async def question_1(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Ты уже подписал(а) все необходимые документы?", reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form_1.no_question_2)

@after_1_month_router.message(F.text, Form_1.no_question_2)
async def no_question_2(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("А обходной лист прошел(а)?")
    await state.set_state(Form_1.no_question_3)

@after_1_month_router.message(F.text, Form_1.no_question_3)
async def no_question_3(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Прошел(а) инструктажи? Какие, расскажешь?")
    await state.set_state(Form_1.no_question_4)

@after_1_month_router.message(F.text, Form_1.no_question_4)
async def no_question_4(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Все ли доступы для работы имеются у тебя? Каких не хватает?")
    await state.set_state(Form_1.no_question_5)

@after_1_month_router.message(F.text, Form_1.no_question_5)
async def no_question_5(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Тебе рассказали  про твои функциональный обязанности?")
    await state.set_state(Form_1.no_question_6)

@after_1_month_router.message(F.text, Form_1.no_question_6)
async def no_question_6(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Они совпадают с тем, что заявляли на этапе собеседования?")
    await state.set_state(Form_1.no_question_7)

@after_1_month_router.message(F.text, Form_1.no_question_7)
async def no_question_7(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("В каком формате получаешь трудовые задачи?")
    await state.set_state(Form_1.no_question_8)

@after_1_month_router.message(F.text, Form_1.no_question_8)
async def no_question_8(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Назначен ли куратор/наставник?")
    await state.set_state(Form_1.no_question_9)

@after_1_month_router.message(F.text, Form_1.no_question_9)
async def no_question_9(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Вы уже начали работу с ним? Опишите в пару словах формат работы? Возможно план работы уже у вас составлен.")
    await state.set_state(Form_1.no_question_10)

@after_1_month_router.message(F.text, Form_1.no_question_10)
async def no_question_10(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Была ли встреча с председателем совета молодежи филиала?")
    await state.set_state(Form_1.no_question_11)

@after_1_month_router.message(F.text, Form_1.no_question_11)
async def no_question_11(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Уже принял участие в каких-либо мероприятиях филиала?")
    await state.set_state(Form_1.no_question_12)

@after_1_month_router.message(F.text, Form_1.no_question_12)
async def no_question_12(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Есть ли у тебя вопросы?")
    await state.set_state(Form_1.result)

@after_1_month_router.message(F.text, Form_1.result)
async def result(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Спасибо за предоставленную информацию!\n"
                             "Куратор изучит ответы и, если потребуется, свяжется с тобой!", 
                             reply_markup = question_kb(message.from_user.id))
    await state.clear()