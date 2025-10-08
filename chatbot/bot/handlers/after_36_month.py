import asyncio
from bot.create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.chat_action import ChatActionSender
from bot.keyboards import ready_kb, question_kb, done_kb # клавиатуры
from datetime import date, timedelta
import os
import django
import sys
from asgiref.sync import sync_to_async


from core.models import Employee, Answer

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 1

# состояния бота
class Form_36(StatesGroup):
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
   result = State()
   
after_36_month_router = Router()

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


@after_36_month_router.message(F.text == "Я заполнил(а)")   
async def end(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Спасибо за обратную связь!\n\nПрограмма адаптации подошла к концу, но я и твой куратор всегда открыты для любых вопросов.\n\nЖелаем тебе успехов и вдохновения на новых этапах твоей профессиональной дороги!\n\nВсё обязательно получится!\n\nПока!!!",
         reply_markup = ReplyKeyboardRemove()
      )
   await state.clear()  

@after_36_month_router.message(Command('after_36_month'))
async def start_poll_after_36_month(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer('Привет!\n\n'
                           'Поздравляю с успешными тремя годами работы в нашей команде! 🎉\n\n'
                           'Уверен, что успехов достигнуто не мало!\n'
                           'Но сегодня отличный повод вспомнить пройденный путь и обсудить дальнейшие планы.\n'
                           'Давай поговорим о том, как тебе работается сейчас, какие успехи достиг, и какие предложения у тебя есть для повышения эффективности и интереса в твоей работе!\n'
                           'Что скажешь? Нажми «Готов»!', reply_markup = await ready_kb(message.from_user.id))
   await state.set_state(Form_36.how_are_you)

@after_36_month_router.message(F.text == "Готов(а)", Form_36.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Назови три наиболее значимых результата твоего третьего года работы.",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Form_36.question_1)

@after_36_month_router.message(F.text, Form_36.question_1)
async def question_1(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_2, "Какие впечатления остались от первого периода работы?", 73)

@after_36_month_router.message(F.text, Form_36.question_2)
async def question_2(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_3, "Какие изменения помогли бы повысить эффективность производственной деятельности?", 74)

@after_36_month_router.message(F.text, Form_36.question_3)
async def question_3(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_4, "Оставляет ли выполнение работы желаемый эффект и приносит удовольствие?", 75)

@after_36_month_router.message(F.text, Form_36.question_4)
async def question_4(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_5, "Имеется ли потребность в дополнительном обучении или развитии?", 76)

@after_36_month_router.message(F.text, Form_36.question_5)
async def question_5(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_6, "Удовлетворяют ли имеющиеся возможности карьерного роста?", 77)
   
@after_36_month_router.message(F.text, Form_36.question_6)
async def question_6(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_7, "Необходима ли поддержка для снижения стрессов и перегрузок?", 78)

@after_36_month_router.message(F.text, Form_36.question_7)
async def question_7(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_8, "Как складываются отношения с руководителем?", 79)

@after_36_month_router.message(F.text, Form_36.question_8)
async def question_8(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.question_9, "Сохраняется ли высокая степень лояльности к компании и желание продолжения сотрудничества?", 80)

@after_36_month_router.message(F.text, Form_36.question_9)
async def question_9(message: Message, state: FSMContext):
   await handle_question(message, state, Form_36.result, "Может есть волнующие моменты, которые тебя беспокоят?", 81)

@after_36_month_router.message(F.text, Form_36.result)
async def result(message: Message, state: FSMContext):
   await end(message, state)