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
class Form_12(StatesGroup):
   how_are_you = State()
   question_1 = State()
   question_2 = State()
   question_3 = State()
   question_4 = State()
   question_5 = State()
   question_6 = State()
   result = State()
   
after_12_month_router = Router()

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
async def finish_poll(message: Message, state: FSMContext, question_id = None):
   if question_id:
      telegram_id = message.from_user.id
      employee = await get_employee(telegram_id)
      await save_answer(employee, message.text, question_id)
   async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Согласно внутренним регламентирующим документам, все молодые специалисты компании проходят психологическое тестирование."
         "тестирование для самоанализа личного профиля.\n\n"
         "Для прохождения теста перейди по следующей ссылке: https://forms.yandex.ru/cloud/665e766290fa7b1d6999c9a8/\n\n"
         "После завершения тестирования вернись в диалог и подтверди выполнение, нажав кнопку «Я заполнил(а)».\n\n",
         reply_markup = done_kb(message.from_user.id)
      )
   await end(message, state)

@after_12_month_router.message(F.text == "Я заполнил(а)")   
async def end(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Спасибо за ваше понимание и активное взаимодействие! До новых встреч!",
         reply_markup = ReplyKeyboardRemove()
      )
   await state.clear()  

@after_12_month_router.message(Command('after_12_month'))
async def start_poll_after_1_month(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer('Привет!\n\n'
                           'Поздравляю с первым трудовым годом в нашей замечательной команде! '
                           'За прошедший год ты стал важной частью коллектива, внес огромный вклад в развитие компании и доказал свою компетентность и профессионализм.\n'
                           'Ты проделал большую работу и наверняка успел накопить много полезных знаний и опыта. \n'
                           'Поделись впечатлениями о первом рабочем году, расскажи о достижениях и успехах, которыми гордишься больше всего. А также поделись идеями, как мы можем сделать нашу совместную работу ещё эффективнее и комфортнее.\n'
                           'Готов(а)? Нажимай кнопку «Готов(а)»', reply_markup = ready_kb(message.from_user.id))
   await state.set_state(Form_12.how_are_you)

@after_12_month_router.message(F.text == "Готов(а)", Form_12.how_are_you)
async def how_are_you(message: Message, state: FSMContext):
   async with ChatActionSender.typing(bot=bot, chat_id=message.chat.id):
      await asyncio.sleep(short_delay)
      await message.answer(
         "Как обстоят дела в производственной среде?",
         reply_markup=ReplyKeyboardRemove()
      )
   await state.set_state(Form_12.question_1)

@after_12_month_router.message(F.text, Form_12.question_1)
async def question_1(message: Message, state: FSMContext):
   await handle_question(message, state, Form_12.question_2, "Какой самый значимый успех ты достиг за этот год и почему именно он особенно важен для тебя?", 39)

@after_12_month_router.message(F.text, Form_12.question_2)
async def question_2(message: Message, state: FSMContext):
   await handle_question(message, state, Form_12.question_3, "o	Есть ли ощущение комфорта и уверенности в рабочих процессах на сегодняшний день?", 40)

@after_12_month_router.message(F.text, Form_12.question_3)
async def question_3(message: Message, state: FSMContext):
   await handle_question(message, state, Form_12.question_4, "Достаточны ли знания и навыки для выполнения поставленных задач?", 41)

@after_12_month_router.message(F.text, Form_12.question_4)
async def question_4(message: Message, state: FSMContext):
   await handle_question(message, state, Form_12.question_5, "Комфортно ли тебе взаимодействовать с руководителем?", 42)

@after_12_month_router.message(F.text, Form_12.question_5)
async def question_5(message: Message, state: FSMContext):
   await handle_question(message, state, Form_12.question_6, "Устраивает ли тебя нынешняя организация твоего рабочего места? Комфортно ли тебе там находиться и продуктивно работать?", 43)

@after_12_month_router.message(F.text, Form_12.question_6)
async def question_6(message: Message, state: FSMContext):
   await handle_question(message, state, Form_12.result, "Может есть волнующие моменты, которые тебя беспокоят?", 44)

@after_12_month_router.message(F.text, Form_12.result)
async def result(message: Message, state: FSMContext):
   await finish_poll(message, state, 45)