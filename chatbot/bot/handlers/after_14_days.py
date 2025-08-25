import asyncio
from bot.create_bot import bot, dp
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, PollAnswer
from aiogram.utils.chat_action import ChatActionSender
from asgiref.sync import sync_to_async
from aiogram.types import Message
from core.models import Employee, Answer, Poll

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 1

POLL_OPTIONS = ["Все отлично! 👍", "Все хорошо! 😊", "Средне", "Хотелось бы, чтоб было лучше …🙁", "Все плохо! 😢"]

# состояния бота
class Form_14(StatesGroup):
   how_are_you = State()
   track_passing = State()
   question_1 = State()
   question_2 = State()
   question_3 = State()
   result = State()
   
after_14_days_router = Router()

# Получает объект сотрудника из базы данных по его telegram id
# Принимает: telegram_id — идентификатор пользователя в telegram
# Возвращает: объект Employee или вызывает исключение, если сотрудник не найден
async def get_employee(telegram_id):
   return await sync_to_async(Employee.objects.get)(telegram_id = telegram_id)

# Сохраняет ответ сотрудника в базу данных
# Принимает: employee — сотрудник, ответивший на вопрос, message_text — текст ответа, question_id — id вопроса в базе данных
async def save_answer(employee, message_text, question_id):
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
         "Спасибо за обратную связь! Обязательно передам все куратору 👌\n"
         "До связи! 💬")
   await state.clear()


@after_14_days_router.message(Command('after_14_days'))
async def start_poll_after_14_days(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer('Приветствую тебя, молодой специалист! 👋\n\n'
                           'Это я – Газоптикум, твой личный цифровой помощник! \n'
                           'Мне интересно, как у тебя дела?\n'
                           'Отметь в опросе ниже ⬇',)
      await message.answer_poll(
         question="Как у тебя дела?",
         options=POLL_OPTIONS,      
         is_anonymous=False,
         allows_multiple_answers=False,
         type="regular"
      )
      await message.answer(
         "Как обстоят дела с организацией твоей производственной деятельности? Опиши в нескольких предложениях ⬇"
      )
      await state.set_state(Form_14.question_3)
      

@after_14_days_router.poll_answer()
async def poll_data(poll_answer: PollAnswer):
   options = POLL_OPTIONS
   selected_option_index = poll_answer.option_ids[0]
   selected_option_text = options[selected_option_index]
   employee = await get_employee(poll_answer.user.id)
   employee_answer = Answer(
      name=selected_option_text,
      login_id=employee.id,
      question_id=46
   )
   await sync_to_async(employee_answer.save)()
   
  

@after_14_days_router.message(F.text, Form_14.question_2)
async def how_are_you(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Как обстоят дела с организацией твоей производственной деятельности? Опиши в нескольких предложениях ⬇",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Form_14.question_3)


@after_14_days_router.message(F.text, Form_14.question_3)
async def question_3(message: Message, state: FSMContext):
   await handle_question(message, state, Form_14.result, "Возможно у тебя появились вопросы?", 48)


@after_14_days_router.message(F.text, Form_14.result)
async def result(message: Message, state: FSMContext):
   await finish_poll(message, state, 49)