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
import os
import re

# время, через которое бот отправит сообщение
short_delay = 1
long_delay = 15

# состояния бота
class Form(StatesGroup):
    surname = State() # ввод фамилии
    name = State() # ввод имени
    patronymic = State() # ввод отчества
    service_number = State() # ввод табельного номера
    branch = State() # выбор филиала
    hire_date = State() # ввод даты трудоустройства
    curator_information = State() # вывод информации о кураторах
    do_task = State() # запрос на выполенение первого задания
    task = State() # выполнение первого задания
    welcome_day_information = State() # вывод информации о welcome-дне
    recommendations = State() # вывод рекомендаций
    
poll_1_router = Router()

@poll_1_router.message(Command('tell_about_myself')) # обработка команды /tell_about_myself
@poll_1_router.message(F.text == 'Рассказать о себе') # обработка текстового сообщения "Рассказать о себе"
# запуск процесса анкетирования, бот запрашивает фамилию
# параметры: message - сообщение от пользователя, state - контекст состояния (в последующих функциях такие же параметры)
async def capture_surname(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer('Введи свою фамилию:', reply_markup = ReplyKeyboardRemove()) # бот отправляет сообщение
    await state.set_state(Form.name) # переход к следующему состоянию

@poll_1_router.message(F.text, Form.name) # обработка текстового сообщения (F.text), с текущим состоянием Form.name
# бот запрашивает имя
async def capture_name(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer('Введи своё имя:') # бот отправляет сообщение
    await state.set_state(Form.patronymic) # переход к следующему состоянию

@poll_1_router.message(F.text, Form.patronymic) # обработка текстового сообщения (F.text), с текущим состоянием Form.patronymic
# бот запрашивает отчество
async def capture_patronymic(message: Message, state: FSMContext):
    await state.update_data(name = message.text)
    async with ChatActionSender.typing(bot=bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer('Введи своё отчество:') # бот отправляет сообщение
    await state.set_state(Form.service_number) # переход к следующему состоянию

@poll_1_router.message(F.text, Form.service_number) # обработка текстового сообщения (F.text), с текущим состоянием Form.service_number
# бот запрашивает табельный номер
async def capture_service_number(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        data = await state.get_data() # получение данных из состояния
        msg_text = (f'{data.get("name")}, укажи свой табельный номер:') # сообщение с запросом табельного номера
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer(msg_text, reply_markup = service_number_kb(message.from_user.id)) # бот отправляет сообщение, появляется клавиатура service_number_kb
    await state.set_state(Form.branch) # переход к следующему состоянию

@poll_1_router.message(F.text, Form.branch) # обработка текстового сообщения (F.text), с текущим состоянием Form.branch
# проводится проверка корректности введенного табельного номера, бот просит выбрать филиал из списка
async def capture_branch(message: Message, state: FSMContext):
    if message.text == "Я не знаю свой табельный номер": # если пользователь нажал на клавиатуре кнопку "Я не знаю свой табельный номер"
        data = await state.get_data() # получение данных из состояния
        msg_text = f'{data.get("name")}, выбери свой филиал из списка:' # сообщение с запросом филиала
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
            await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
            await message.answer(msg_text, reply_markup = branches_kb()) # бот отправляет сообщение, появляется инлайн клавиатура branches_kb
        await state.set_state(Form.hire_date) # переход к следующему состоянию
        return
    if not message.text.isdigit(): # если пользователь ввел не только цифры
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
            await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
            await message.reply('Табельный номер должен содержать только цифры. Пожалуйста, введите шестизначное число:') # бот отправляет сообщение
        return
    if len(message.text) != 6: # если пользователь ввел не 6 цифр
        async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
            await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
            await message.reply('Табельный номер должен состоять из 6 цифр. Пожалуйста, введите шестизначное число:') # бот отправляет сообщение
        return
    service_number = message.text # сохранение табельного номера
    await state.update_data(service_number = service_number) # запись корректного номера в данные состояния
    data = await state.get_data() # получение данных из состояния
    msg_text = f'{data.get("name")}, выбери свой филиал из списка:' # сообщение с запросом филиала
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer(msg_text, reply_markup = branches_kb()) # бот отправляет сообщение, появляется инлайн клавиатура branches_kb
    await state.set_state(Form.hire_date) # переход к следующему состоянию

@poll_1_router.callback_query(F.data.startswith("branch_"), Form.hire_date) # обработка данных callback, начинающихся с "branch_", с текущим состоянием Form.hire_date
# бот запрашивает дату трудоустройства
# параметры: объект CallbackQuery с информацией о callback-запросе, state - контекст состояния
async def capture_hire_date(callback: CallbackQuery, state: FSMContext):
    branch = callback.data.replace("branch_", "") # извлечение названия филиала из callback.data, удаляя префикс "branch_"
    await state.update_data(branch = branch) # запись названия филиала в данные состояния
    await callback.message.answer(text = f"Выбран филиал: {branch}", reply_markup = ReplyKeyboardRemove()) # бот отправляет сообщение
    data = await state.get_data() # получение данных из состояния
    msg_text = f'{data.get("name")}, укажи дату приёма в компанию в формате DD.MM.YYYY (например, 01.01.2025):' # сообщение с запросом даты трудоустройства
    await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
    await callback.message.answer(msg_text) # бот отправляет сообщение
    await state.set_state(Form.curator_information) # переход к следующему состоянию
    await callback.answer() # подтверждение получения callback-запроса

@poll_1_router.message(F.text, Form.curator_information) # обработка текстового сообщения (F.text), с текущим состоянием Form.curator_information
# бот присылает информацию о кураторе
async def capture_curator_information(message: Message, state: FSMContext):
    date_pattern = r'^\d{2}\.\d{2}\.\d{4}$' # регулярное выражение для проверки формата даты
    if not re.match(date_pattern, message.text): # если введенный текст не соответствует шаблону даты
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.reply('Неверный формат даты. Пожалуйста, введите дату в формате DD.MM.YYYY:') # бот отправляет сообщение
        return
    await state.update_data(hire_date = message.text) # запись даты трудоустройства в данные состояния
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer('Спасибо за ответы!') # бот отправляет сообщение
        # data = await state.get_data() # получение данных из состояния
        # await state.update_data(name = data.get("name")) # запись даты трудоустройства в данные состояния
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(long_delay) # бот отправляет сообщение через время long_delay
        await message.answer("В нашей компании адаптация новых сотрудников — приоритетная задача, "
                             "ведь люди — наш главный ресурс.\n\n"
                             "В течение трех лет тебя будет поддерживать куратор, "
                             "вместе с которым вы решите все возникающие вопросы и обеспечите "
                             "соблюдение всех нормативных требований регламентирующих документов.\n\n"
                             "Ты не просто новичок, ты — Молодой Специалист!") # бот отправляет сообщение
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(long_delay) # бот отправляет сообщение через время long_delay
        await message.answer("Кто такой куратор? Смотри видеоролик ниже!\n\n"
                             "После ознакомления нажимай кнопку «Ознакомился(ась)».") # бот отправляет сообщение
        video_file = FSInputFile(path = os.path.join(media_dir, 'test_video.mp4')) # создание объекта видеофайла из указанного пути 
        await message.answer_video(video = video_file, reply_markup = reviewed_kb(message.from_user.id)) # бот отправляет видео, появляется клавиатура reviewed_kb
    await state.set_state(Form.do_task) # переход к следующему состоянию

@poll_1_router.message(F.text == 'Ознакомился(ась)', Form.do_task) # обработка текстового сообщения "Ознакомился(ась)", с текущим состоянием Form.do_task
# бот просит выполнить первое задание
async def capture_do_task(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        data = await state.get_data() # получение данных из состояния
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer(f'{data.get("name")}, отлично! Теперь мы знаем друг о друге лучше!\n\n'
                             'Лично с куратором ты познакомишься позже, а пока прошу выполнить первое задание! '
                             'Для этого нажми на кнопку \"Задание\".', reply_markup = task_kb(message.from_user.id)) # бот отправляет сообщение, появляется клавиатруа task_kb
    await state.set_state(Form.task) # переход к следующему состоянию

@poll_1_router.message(F.text == "Задание", Form.task) # обработка текстового сообщения "Задание", с текущим состоянием Form.task
# бот присылает первое задание
async def capture_task(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer("Согласно внутренним регламентирующим документам,"
                             "все молодые специалисты обязаны компании проходят психологическое тестирование.\n\n"
                             "Для прохождения теста перейди по следующей ссылке: <a href='https://psytests.org/stress/ouslu-run.html'>психологический тест</a>.\n\n"
                             "После завершения тестирования вернись в диалог и подтверди выполнение, нажав кнопку \"Я заполнил(а)\".", 
                             reply_markup = done_kb(message.from_user.id), parse_mode = "HTML") # бот отправляет сообщение с ссылкой, появляется клавиатура done_kb
    await state.set_state(Form.welcome_day_information) # переход к следующему состоянию

@poll_1_router.message(F.text == "Я заполнил(а)", Form.welcome_day_information) # обработка текстового сообщения "Я заполнил(а)", с текущим состоянием Form.welcome_day_information
# бот присылает информацию о welcome-дне
async def capture_welcome_day_information(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        data = await state.get_data() # получение данных из состояния
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer(f'{data.get("name")}, спасибо за прохождение тестирования.\n\n'
                             'Далее тебя ожидает встреча с куратором в рамках Welcome-дня, '
                             'где будут представлены увлекательные сведения о возможностях твоего развития в компании. '
                             'Дата и время встречи будут дополнительно сообщены куратором.\n\n' 
                             'Не упусти возможность!', reply_markup = ReplyKeyboardRemove()) # бот отправляет сообщение, скрывается клавиатура 
        await asyncio.sleep(long_delay) # бот отправляет сообщение через время long_delay
        await message.answer(f'{data.get("name")}, поздравляю с началом нового этапа и желаю успехов в профессиональных начинаниях!\n\n'
                             'Но чтобы первые трудовые дни прошли гладко, предлагаю несколько полезных советов, '
                             'просто нажми кнопку \"Получить рекомендации\".', reply_markup = recommendations_kb(message.from_user.id)) # бот отправляет сообщение, появляется клавиатура recommendations_kb
    await state.set_state(Form.recommendations) # переход к следующему состоянию

@poll_1_router.message(F.text == "Получить рекомендации", Form.recommendations) # обработка текстового сообщения "Получить рекомендации", с текущим состоянием Form.recommendations
# бот даёт рекомендации
async def capture_recommendations(message: Message, state: FSMContext):
    async with ChatActionSender.typing(bot = bot, chat_id = message.chat.id): # создается видимость того, что бот печатает сообщение
        await asyncio.sleep(short_delay) # бот отправляет сообщение через время short_delay
        await message.answer("Если возникнут вопросы, смело обращайся в чат — мы с куратором оперативно предоставим необходимую помощь.\n\n"
                             "Для написания вопроса напиши \"/хочузадатьвопрос\" или нажми на кнопку \"Хочу задать вопрос\".\n\n"
                             "До встречи!", reply_markup = question_kb(message.from_user.id)) # бот отправляет сообщение, появляется клавиатура question_kb
    await state.clear() # очистка памяти