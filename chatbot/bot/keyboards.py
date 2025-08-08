from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from create_bot import get_curators_telegram_ids
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import os
import django
import sys
from asgiref.sync import sync_to_async
import asyncio

sys.path.append(r'C:\Users\oxina\OneDrive\Рабочий стол\работа\chat-bot\chatbot')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'chatbot.settings')
django.setup()

async def is_curator():
    curators = await get_curators_telegram_ids()
    return curators

# Асинхронное получение списка филиалов
async def get_branches():
    from core.models import Filial
    @sync_to_async
    def get_branches_sync():
        return list(Filial.objects.all().order_by('name'))
    
    return await get_branches_sync()

# Инлайн клавиатура с филиалами
async def branches_kb() -> InlineKeyboardMarkup:
    branches = await get_branches()
    buttons = [
        InlineKeyboardButton(text=branch.name, callback_data=f"branch_{branch.id}") 
        for branch in branches
    ]
    return InlineKeyboardMarkup(inline_keyboard=[[button] for button in buttons])
# def branches_kb() -> InlineKeyboardMarkup:
#     # список с филиалами
#     branches = [
#         "Администрация",
#         "Алданское ЛПУМГ",
#         "Александровское ЛПУМГ",
#         "Алтайское ЛПУМГ",
#         "Амурское ЛПУМГ",
#         "Барабинское ЛПУМГ",
#         "Инженерно-технический центр",
#         "Иркутское ЛПУМГ",
#         "Камчатское ЛПУМГ",
#         "Кемеровское ЛПУМГ",
#         "Корпоративный институт",
#         "Ленское ЛПУМГ",
#         "Магистральное ЛПУМГ",
#         "Нерюнгринское ЛПУМГ",
#         "Новокузнецкое ЛПУМГ",
#         "Новосибирское ЛПУМГ",
#         "Омское ЛПУМГ",
#         "Приморское ЛПУМГ",
#         "Сахалинское ЛПУМГ",
#         "Свободненское ЛПУМГ",
#         "Сковородинское ЛПУМГ",
#         "Томское ЛПУМГ",
#         "Управление АВР",
#         "Управление АВР №2",
#         "Управление МТСиК",
#         "Управление ТТиСТ",
#         "Юргинское ЛПУМГ",
#         "Хабаровское ЛПУМГ"
#     ]
#     buttons = [
#         InlineKeyboardButton(text = branch, callback_data = f"branch_{branch}") 
#         for branch in branches
#     ]
#     return InlineKeyboardMarkup(inline_keyboard = [[button] for button in buttons])

# клавиатура с кнопкой "Рассказать о себе"
def tell_about_myself_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Рассказать о себе")]
    ]
    if user_telegram_id in is_curator():
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Я не знаю свой табельный номер"
def service_number_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Я не знаю свой табельный номер")]
    ]
    if user_telegram_id in is_curator():
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Ознакомился(ась)"
def reviewed_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Ознакомился(ась)")]
    ]
    if user_telegram_id in is_curator():
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Задание"
def task_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Задание")]
    ]
    if user_telegram_id in is_curator():
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Я заполнил(а)"
def done_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Я заполнил(а)")]
    ]
    if user_telegram_id in is_curator():
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Получить рекомендации"
async def recommendations_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Получить рекомендации")]
    ]
    curators = await is_curator()  # Получаем список кураторов
    if user_telegram_id in curators:
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Хочу задать вопрос"
async def question_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Хочу задать вопрос")],
        [KeyboardButton(text = "Вопросов нет")]
    ]
    curators = await is_curator()  # Получаем список кураторов
    if user_telegram_id in curators:
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура с кнопкой "Готов(а)"
async def ready_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Готов(а)")]
    ]
    curators = await is_curator()  # Получаем список кураторов
    if user_telegram_id in curators:
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура да/нет
async def yes_or_no_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Да")],
        [KeyboardButton(text = "Нет")]
    ]
    curators = await is_curator()  # Получаем список кураторов
    if user_telegram_id in curators:
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

# клавиатура да/нет/не знаю
def yes_or_no_maybe_kb(user_telegram_id: int):
    kb_list = [
        [KeyboardButton(text = "Да")],
        [KeyboardButton(text = "Нет")],
        [KeyboardButton(text = "Не имею понятия, что за приложение")]
    ]
    if user_telegram_id in is_curator():
        kb_list.append([KeyboardButton(text = "Создать рассылку")]) # кнопка, которая видна только админу
    keyboard = ReplyKeyboardMarkup(
        keyboard = kb_list,
        resize_keyboard = True, # автоматически подгоняет размер кнопок под экран
        one_time_keyboard = True # клавиатура скроется после нажатия
    )
    return keyboard

#клавиатура подтверждения
def accept_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Подтвердить")],
            [KeyboardButton(text="Отредактировать")],
            [KeyboardButton(text="Добавить ещё файлы")]
        ],
        resize_keyboard=True
    )

#клавиатура для прикрепления вложений
def attachment_kb():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Не прикреплять")],
        ],
        resize_keyboard=True
    )    