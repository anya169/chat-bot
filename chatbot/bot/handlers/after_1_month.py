import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from datetime import date, timedelta
from keyboards import ready_kb, yes_or_no_kb, question_kb, yes_or_no_maybe_kb # клавиатуры
import os
import django
import sys
from asgiref.sync import sync_to_async

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
from core.models import Employee, Answer, Poll

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 1

# состояния бота
class Form_1(StatesGroup):
    how_are_you = State()
    track_passing = State()
    question_1 = State()
    yes_question_2 = State()
    yes_question_3 = State()
    question_for_all = State()
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
    question_12 = State()
    question_13 = State()
    question_14 = State()
    result = State()
    
after_1_month_router = Router()

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
        submission_date = timedelta(days = days_passed),
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
            "Все твои ответы будут внимательно рассмотрены куратором. Если понадобится дополнительная поддержка или обсуждение отдельных моментов, он обязательно свяжется с тобой.",
            reply_markup = await question_kb(message.from_user.id)
        )
    await state.clear()

@after_1_month_router.message(Command('after_1_month'))
async def start_poll_after_1_month(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Привет!\n\n'
                             'Поздравляю тебя с успешным стартом в нашей команде — прошёл уже целый месяц! \n'
                             'Для того, чтобы мы могли вместе увидеть, насколько успешно идёт процесс адаптации и интеграции, предлагаю заполнить небольшой опрос по чек-листу обратной связи.\n'
                             'Нажми кнопку «Готов(а)!», и мы начнем наш диалог!', reply_markup = ready_kb(message.from_user.id))
    await state.set_state(Form_1.how_are_you)

@after_1_month_router.message(F.text == "Готов(а)", Form_1.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(
            "Как обстоят дела в производственной среде?",
            reply_markup=ReplyKeyboardRemove()
        )
    await state.set_state(Form_1.question_1)

@after_1_month_router.message(F.text, Form_1.track_passing)
async def track_passing(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_1, "Удалось ли зайти в мобильное приложение ГИД?", 2, yes_or_no_maybe_kb(message.from_user.id))

@after_1_month_router.message(
    (F.text.lower() == "да"),
    Form_1.question_1  
)
async def question_1_yes(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.yes_question_2, "Был ли полезным и информативным для тебя трек в приложении?", 3)

@after_1_month_router.message(F.text, Form_1.yes_question_2)
async def yes_question_2(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.yes_question_3, "Расскажи, что больше всего заинтересовало?", 4)

@after_1_month_router.message(F.text, Form_1.yes_question_3)
async def yes_question_3(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_for_all, "Есть ли такая информация, которой не хватило?", 5)

@after_1_month_router.message(F.text, Form_1.question_for_all)
async def question_1_no(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_2, "Ты наверняка уже подписал (а) все необходимые документы для трудоустройства?", 6)

@after_1_month_router.message(
    F.text.in_(["Нет", "Не имею понятия, что за приложение"]), 
    Form_1.question_1
)
async def question_1_no(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_2, "Ты наверняка уже подписал (а) все необходимые документы для трудоустройства?", 6)

@after_1_month_router.message(F.text, Form_1.question_2)
async def question_2(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_3, "А обходной лист прошел(а)?", 7)

@after_1_month_router.message(F.text, Form_1.question_3)
async def question_3(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_4, "Прошел(а) инструктажи? Какие, расскажешь?", 8)

@after_1_month_router.message(F.text, Form_1.question_4)
async def question_4(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_5, "Расскажи про рабочее место. Какое оно у тебя?", 9)

@after_1_month_router.message(F.text, Form_1.question_5)
async def question_5(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_6, "Все ли необходимое для работы есть в нем?", 10)

@after_1_month_router.message(F.text, Form_1.question_6)
async def question_6(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_7, "Все ли доступы для работы имеются у тебя? ПК, пропуск? Каких не хватает?", 11)
    
@after_1_month_router.message(F.text, Form_1.question_7)
async def question_7(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_8, "Тебе рассказали про твои функциональные обязанности?", 12)

@after_1_month_router.message(F.text, Form_1.question_8)
async def question_8(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_9, "Они совпадают с тем, что заявляли на этапе собеседования?", 13)

@after_1_month_router.message(F.text, Form_1.question_9)
async def question_9(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_10, "В каком формате получаешь трудовые задачи?", 14)

@after_1_month_router.message(F.text, Form_1.question_10)
async def question_10(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_11, "Назначен ли куратор/наставник?", 15)

@after_1_month_router.message(F.text, Form_1.question_11)
async def question_11(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_12, 
    "Вы уже начали работу с ним? Опишите в пару слов формат работы? Возможно план работы уже у вас составлен.", 16)

@after_1_month_router.message(F.text, Form_1.question_12)
async def question_12(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_13, "Была ли встреча с председателем совета молодежи филиала?", 17)

@after_1_month_router.message(F.text, Form_1.question_13)
async def question_13(message: Message, state: FSMContext):
    await handle_question(message, state, Form_1.question_14, "Уже принял(а) участие в каких-либо мероприятиях филиала?", 18)

@after_1_month_router.message(F.text, Form_1.question_14)
async def final_questions(message: Message, state: FSMContext):
    question_id = 5 if await state.get_state() == Form_1.question_for_all else 19
    await handle_question(message, state, Form_1.result, "Есть ли у тебя вопросы?", question_id)

@after_1_month_router.message(F.text, Form_1.result)
async def result(message: Message, state: FSMContext):
    await finish_poll(message, state, 19)