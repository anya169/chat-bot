import asyncio
from create_bot import bot
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import State, StatesGroup
from aiogram.types import Message, ReplyKeyboardRemove, FSInputFile
from aiogram.utils.chat_action import ChatActionSender
from keyboards import service_number_kb, reviewed_kb, task_kb, done_kb, recommendations_kb, question_kb, branches_kb # клавиатуры
from create_bot import media_dir # медиа
from aiogram.types import CallbackQuery
import re
from datetime import datetime
import os
import django
import sys
from asgiref.sync import sync_to_async

sys.path.append('C:/chat-bot/chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()
from core.models import Employee, Filial

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 1

# состояния бота
class Form(StatesGroup):
    surname = State()
    name = State()
    patronymic = State()
    service_number = State()
    branch = State()
    hire_date = State()
    curator_information = State()
    do_task = State()
    task = State()
    welcome_day_information = State()
    recommendations = State()
    
registration_router = Router()

@registration_router.message(Command('tell_about_myself')) # обработка команды /tell_about_myself
@registration_router.message(F.text == 'Рассказать о себе') # обработка текстового сообщения "Рассказать о себе"
# запуск процесса анкетирования, бот запрашивает фамилию
# параметры: message - сообщение от пользователя, state - контекст состояния (в последующих функциях такие же параметры)
async def capture_surname(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Введи свою фамилию:', reply_markup = ReplyKeyboardRemove())
    await state.set_state(Form.name)

@registration_router.message(F.text, Form.name) # обработка текстового сообщения (F.text), с текущим состоянием Form.name
# бот запрашивает имя
async def capture_name(message: Message, state: FSMContext):
    surname = message.text
    if re.search(r'\d', surname):
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await asyncio.sleep(short_delay)
            await message.answer("Не похоже на фамилию. Попробуйте еще раз:")
        return
    await state.update_data(surname = surname)
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Введи своё имя:')
    await state.set_state(Form.patronymic)

@registration_router.message(F.text, Form.patronymic) # обработка текстового сообщения (F.text), с текущим состоянием Form.patronymic
# бот запрашивает отчество
async def capture_patronymic(message: Message, state: FSMContext):
    name = message.text
    if re.search(r'\d', name):
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await asyncio.sleep(short_delay)
            await message.answer("Не похоже на имя. Попробуйте еще раз:")
        return
    await state.update_data(name = name)
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Введи своё отчество:')
    await state.set_state(Form.service_number)

@registration_router.message(F.text, Form.service_number) # обработка текстового сообщения (F.text), с текущим состоянием Form.service_number
# бот запрашивает табельный номер
async def capture_service_number(message: Message, state: FSMContext):
    patronymic = message.text
    if re.search(r'\d', patronymic):
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await asyncio.sleep(short_delay)
            await message.answer("Не похоже на отчество. Попробуйте еще раз:")
        return
    await state.update_data(patronymic = patronymic)
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        data = await state.get_data()
        msg_text = (f'{data.get("name")}, укажи свой табельный номер:')
        await asyncio.sleep(short_delay)
        await message.answer(msg_text, reply_markup = service_number_kb())
    await state.set_state(Form.branch)

@registration_router.message(F.text, Form.branch) # обработка текстового сообщения (F.text), с текущим состоянием Form.branch
# проводится проверка корректности введенного табельного номера, бот просит выбрать филиал из списка
async def capture_branch(message: Message, state: FSMContext):
    if message.text == "Я не знаю свой табельный номер":
        data = await state.get_data()
        msg_text = f'{data.get("name")}, выбери свой филиал из списка:'
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await asyncio.sleep(short_delay)
            await message.answer(msg_text, reply_markup = await branches_kb())
        await state.set_state(Form.hire_date)
        return
    if not message.text.isdigit():
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await asyncio.sleep(short_delay)
            await message.reply('Табельный номер должен содержать только цифры. Пожалуйста, введите шестизначное число:')
        return
    if len(message.text) != 6:
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
            await asyncio.sleep(short_delay)
            await message.reply('Табельный номер должен состоять из 6 цифр. Пожалуйста, введите шестизначное число:')
        return
    service_number = message.text
    await state.update_data(service_number = service_number)
    data = await state.get_data()
    msg_text = f'{data.get("name")}, выбери свой филиал из списка:'
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer(msg_text, reply_markup = await branches_kb())
    await state.set_state(Form.hire_date)

@registration_router.callback_query(F.data.startswith("branch_"), Form.hire_date) # обработка данных callback, начинающихся с "branch_", с текущим состоянием Form.hire_date
# бот запрашивает дату трудоустройства
# параметры: объект CallbackQuery с информацией о callback-запросе, state - контекст состояния
async def capture_hire_date(callback: CallbackQuery, state: FSMContext):
    branch = callback.data.replace("branch_", "") # извлечение названия филиала из callback.data, удаляя префикс "branch_"
    await state.update_data(branch = branch)
    # await callback.message.answer(text = f"Выбран филиал: {branch}", reply_markup = ReplyKeyboardRemove())
    data = await state.get_data()
    msg_text = f'{data.get("name")}, укажи дату приёма в компанию в формате DD.MM.YYYY (например, 01.01.2025):'
    await asyncio.sleep(short_delay)
    await callback.message.answer(msg_text)
    await state.set_state(Form.curator_information)
    await callback.answer()

@registration_router.message(F.text, Form.curator_information) # обработка текстового сообщения (F.text), с текущим состоянием Form.curator_information
# бот присылает информацию о кураторе
async def capture_curator_information(message: Message, state: FSMContext):
    date_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
    if not re.match(date_pattern, message.text):
        await asyncio.sleep(short_delay)
        await message.reply('Неверный формат даты. Пожалуйста, введите дату в формате DD.MM.YYYY:')
        return
    try:
        hire_date = datetime.strptime(message.text, "%d.%m.%Y").date()
    except ValueError:
        await asyncio.sleep(short_delay)
        await message.reply('Неверный формат даты. Пожалуйста, введите дату в формате DD.MM.YYYY:')
        return
    await state.update_data(hire_date = message.text)
    data = await state.get_data()
    try:
        filial, _ = await sync_to_async(Filial.objects.get)(name=data.get('branch'))
        employee = await sync_to_async(Employee.objects.create)(
            num_tab=data.get('service_number', 'Не указан'),
            name=f"{data.get('surname', '')} {data.get('name', '')} {data.get('patronymic', '')}".strip(),
            filial=filial,
            hire_date=hire_date,
            telegram_id=message.from_user.id,
            telegram_registration_date=datetime.now().date()
        )
        await asyncio.sleep(short_delay)
    except Exception as e:
        print(f"Ошибка при сохранении данных: {e}")
        await asyncio.sleep(short_delay)
        await message.answer('Произошла ошибка при сохранении ваших данных. Пожалуйста, попробуйте позже.')
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer('Спасибо за ответы!')
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(long_delay)
        await message.answer("В нашей компании адаптация новых сотрудников — приоритетная задача, "
                             "ведь люди — наш главный ресурс.\n\n"
                             "В течение трех лет тебя будет поддерживать куратор, "
                             "вместе с которым вы решите все возникающие вопросы и обеспечите "
                             "соблюдение всех нормативных требований регламентирующих документов.\n\n"
                             "Ты не просто новичок, ты — Молодой Специалист!")
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(long_delay)
        await message.answer("Кто такой куратор? Смотри видеоролик ниже!\n\n"
                             "После ознакомления нажимай кнопку «Ознакомился(ась)».")
        video_file = FSInputFile(path = os.path.join(media_dir, 'test_video.mp4'))
        await message.answer_video(video = video_file, reply_markup = reviewed_kb())
    await state.set_state(Form.do_task)

@registration_router.message(F.text == 'Ознакомился(ась)', Form.do_task) # обработка текстового сообщения "Ознакомился(ась)", с текущим состоянием Form.do_task
# бот просит выполнить первое задание
async def capture_do_task(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        data = await state.get_data()
        await asyncio.sleep(short_delay)
        await message.answer(f'{data.get("name")}, отлично! Теперь мы знаем друг о друге лучше!\n\n'
                             'Лично с куратором ты познакомишься чуть позже, а пока прошу выполнить первое задание! '
                             'Для этого нажми на кнопку \"Задание\".', reply_markup = task_kb())
    await state.set_state(Form.task)

@registration_router.message(F.text == "Задание", Form.task) # обработка текстового сообщения "Задание", с текущим состоянием Form.task
# бот присылает первое задание
async def capture_task(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Согласно внутренним регламентирующим документам,"
                             "все молодые специалисты обязаны компании проходят психологическое тестирование.\n\n"
                             "Для прохождения теста перейди по следующей ссылке: <a href='https://forms.yandex.ru/cloud/665e7565d046880010428699/'>психологический тест</a>.\n\n"
                             "После завершения тестирования вернись в диалог и подтверди выполнение, нажав кнопку \"Я заполнил(а)\".", 
                             reply_markup = await done_kb(message.from_user.id), parse_mode = "HTML")
    await state.set_state(Form.welcome_day_information)

@registration_router.message(F.text == "Я заполнил(а)", Form.welcome_day_information) # обработка текстового сообщения "Я заполнил(а)", с текущим состоянием Form.welcome_day_information
# бот присылает информацию о welcome-дне
async def capture_welcome_day_information(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        data = await state.get_data()
        await asyncio.sleep(short_delay)
        await message.answer(f'{data.get("name")}, спасибо за прохождение тестирования.\n\n'
                             'Далее тебя ожидает встреча с куратором в рамках Welcome-дня, '
                             'где будут представлены увлекательные сведения о возможностях твоего развития в компании. '
                             'Дата и время встречи будут дополнительно сообщены куратором.\n\n' 
                             'Не упусти возможность!', reply_markup = ReplyKeyboardRemove())
        await asyncio.sleep(long_delay)
        await message.answer('А пока время погрузиться в рабочую среду!\n'
                             'Чтобы первые трудовые дни прошли гладко, предлагаю несколько полезных советов, '
                             'просто нажми кнопку \"Получить рекомендации\".', reply_markup = await recommendations_kb(message.from_user.id))
    await state.set_state(Form.recommendations)

@registration_router.message(F.text == "Получить рекомендации", Form.recommendations) # обработка текстового сообщения "Получить рекомендации", с текущим состоянием Form.recommendations
# бот даёт рекомендации
async def capture_recommendations(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id):
        await asyncio.sleep(short_delay)
        await message.answer("Если возникнут вопросы, смело обращайся в чат — мы с куратором оперативно предоставим необходимую помощь.\n\n"
                             "Для написания вопроса напиши \"/askquestion\" или нажми на кнопку \"Хочу задать вопрос\".\n\n"
                             "До встречи!", reply_markup = await question_kb(message.from_user.id))
    await state.clear()
